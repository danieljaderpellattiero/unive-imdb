import csv


class Utils:

	@staticmethod
	def split_file_by_rows(input_file, output_prefix, record_amount, file_limit, encoding):
		try:
			with open(input_file, 'r', encoding=encoding) as file:
				lines = []
				file_count = 0
				header = file.readline()
				for line in file:
					if file_count < file_limit:
						lines.append(line)
						if len(lines) == record_amount:
							output_file = f"{output_prefix}_{file_count}.tsv"
							with open(output_file, 'w', encoding=encoding) as output:
								output.write(header)
								output.writelines(lines)
							file_count += 1
							lines = []
					else:
						break
				if lines:
					output_file = f"{output_prefix}_{file_count}.tsv"
					with open(output_file, 'w', encoding=encoding) as output:
						output.write(header)
						output.writelines(lines)

		except UnicodeDecodeError as e:
			print(f"Error reading file {input_file}: {e}")

	@staticmethod
	def filter_file_by_id(input_filter_file, input_target_file, output_file, encoding):
		record_ids = set()
		filtered_records = []
		with open(input_filter_file, 'r', newline='', encoding=encoding) as file:
			parser = csv.DictReader(file, delimiter='\t')
			for row in parser:
				record_ids.add(row['tconst'])
		with open(input_target_file, 'r', newline='', encoding=encoding) as file:
			found_ids = 0
			reader = csv.DictReader(file, delimiter='\t')
			headers = reader.fieldnames
			for row in reader:
				if found_ids == len(record_ids):
					break
				if row['tconst'] in record_ids:
					filtered_records.append(row)
					found_ids += 1
		with open(output_file, 'w', newline='', encoding=encoding) as file:
			writer = csv.DictWriter(file, fieldnames=headers, delimiter='\t')
			writer.writeheader()
			writer.writerows(filtered_records)
