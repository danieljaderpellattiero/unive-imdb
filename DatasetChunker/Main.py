from Utils import Utils

if __name__ == "__main__":
	encoding = 'utf-8'
	input_file = "title.ratings.tsv"
	output_prefix = "title_ratings"
	file_limit = 1
	record_amount = 1000

	Utils.split_file_by_rows(input_file, output_prefix, record_amount, file_limit, encoding)
	Utils.filter_file_by_id("title_ratings_0.tsv", "title.basics.tsv", "title_basics_0.tsv", encoding)
	exit(0)
