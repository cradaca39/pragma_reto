import os

def merge_csv_files():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Sube un nivel
    uploads_dir = os.path.join(base_dir, 'uploads')
    result_dir = os.path.join(os.path.dirname(__file__), 'result')
    output_file = os.path.join(result_dir, 'merged.csv')

    os.makedirs(result_dir, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            if os.path.isfile(file_path) and filename.endswith('.csv'):
                with open(file_path, 'r', encoding='utf-8') as infile:
                    lines = infile.readlines()
                    for line in lines[1:]:
                        outfile.write(line.rstrip('\r\n') + '\n')