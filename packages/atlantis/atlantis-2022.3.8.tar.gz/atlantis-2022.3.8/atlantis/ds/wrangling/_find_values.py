from pyspark.sql import DataFrame as SparkDF
from pyspark.sql import functions as f
from pyspark.sql.types import StringType, BooleanType
from pandas import DataFrame as PandasDF
import validators
from .union import union
from ...text import get_domain_and_tld


@f.udf(StringType())
def get_domain_and_tld_column(url):
	if url is not None:
		return get_domain_and_tld(url)
	else:
		return None


def find_values(data, value_types):
	"""
	finds domains, emails, or ips
	returns a dataframe with three columns: column_name, string_type, value
	if df has columns: parent_domain, email_address, ip_address, child_domain
	with values that match those
	if string_type=['domain']
	the returning dataframe will have column_name with values like parent_domain and child_domain
	string_type as domain
	with domains from those columns in the value column

	:type data: PandasDF or SparkDF
	:type value_types: list[str] or str
	:rtype: PandasDF or SparkDF
	"""

	dataframes = []

	if isinstance(data, SparkDF):

		for string_type in value_types:
			if string_type == 'domain':
				@f.udf(StringType())
				def get_value_column(x):
					try:
						return get_domain_and_tld(x)
					except:
						return None
			else:
				get_value_column = None

			is_valid = getattr(validators, string_type)

			@f.udf(BooleanType())
			def get_is_valid_column(x):
				try:
					if is_valid(x):
						return True
					else:
						return False
				except:
					return False

			for col in data.columns:

				if get_value_column is None:
					df = data.select(
						f.lit(string_type).alias('string_type'), f.lit(col).alias('column'),
						f.col(col).alias('value')
					)
				else:
					df = data.select(
						f.lit(string_type).alias('string_type'), f.lit(col).alias('column'),
						get_value_column(col).alias('value')
					)

				df = df.withColumn('is_valid', get_is_valid_column('value'))
				dataframes.append(df)

		return union(*dataframes, n_jobs=4).filter(f.col('is_valid')).drop('is_valid')

	elif isinstance(data, PandasDF):

		for string_type in value_types:
			if string_type == 'domain':
				def get_value_column(x):
					try:
						return get_domain_and_tld(x)
					except:
						return None
			else:
				get_value_column = None

			_is_valid = getattr(validators, string_type)
			def is_valid(x):
				try:
					return _is_valid(x)
				except:
					return False

			for col in data.columns:
				df = data[[col]].copy()
				df['string_type'] = string_type
				df['column'] = col
				if get_value_column is None:
					df['value'] = df[col]
				else:
					df['value'] = df[col].apply(get_value_column)

				df['is_valid'] = df['value'].apply(is_valid)
				dataframes.append(df)

		result = union(*dataframes, n_jobs=4)
		return result[result['is_valid']].reset_index(drop=True)

	else:
		raise TypeError(f'data of type {type(data)} is not supported!')
