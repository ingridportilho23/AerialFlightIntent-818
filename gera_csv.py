import os
import csv
import ffmpeg
from datetime import datetime

def get_video_duration(file_path):
    try:
        probe = ffmpeg.probe(file_path)
        duration = float(probe['format']['duration'])
        return duration
    except Exception as e:
        print(f"Could not get duration for {file_path}: {e}")
        return 0

def rename_files_and_create_csv(base_directory):
    metadata_file = os.path.join(base_directory, 'metadata.csv')
    with open(metadata_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['FileName', 'FileSize', 'ModificationDate', 'Duration', 'Class'])  # Cabeçalho do CSV

        for class_dir in os.listdir(base_directory):
            class_path = os.path.join(base_directory, class_dir)
            if os.path.isdir(class_path):
                file_count = 1
                for filename in os.listdir(class_path):
                    if filename.endswith('.mp4') and class_dir!= "Não classificados":
                        old_mp4_path = os.path.join(class_path, filename)
                        new_mp4_name = f'aviao_{class_dir}_{file_count}.mp4'
                        new_mp4_path = os.path.join(class_path, new_mp4_name)

                        old_csv_name = filename.replace('.mp4', '.csv')
                        old_csv_path = os.path.join(class_path, old_csv_name)
                        new_csv_name = f'aviao_{class_dir}_{file_count}.csv'
                        new_csv_path = os.path.join(class_path, new_csv_name)

                        # Obter duração antes de renomear
                        duration = get_video_duration(old_mp4_path)
                        file_size = os.path.getsize(old_mp4_path)
                        modification_date = datetime.fromtimestamp(os.path.getmtime(old_mp4_path)).strftime('%Y-%m-%d %H:%M:%S')

                        # Renomear arquivos
                        if not os.path.exists(new_mp4_path):
                            os.rename(old_mp4_path, new_mp4_path)
                            print(f'Renamed: {filename} to {new_mp4_name}')
                        else:
                            print(f'Skipped: {new_mp4_name} already exists')

                        if os.path.exists(old_csv_path):
                            if not os.path.exists(new_csv_path):
                                os.rename(old_csv_path, new_csv_path)
                                print(f'Renamed: {old_csv_name} to {new_csv_name}')
                            else:
                                print(f'Skipped: {new_csv_name} already exists')
                        else:
                            print(f'Skipped: {old_csv_name} does not exist')

                        # Escrever metadados no CSV
                        writer.writerow([new_mp4_name, file_size, modification_date, duration, class_dir])
                        print(f'Added metadata for {new_mp4_name}')

                        # Incrementar a contagem de arquivos
                        file_count += 1

base_directory_path = r'C:\Users\yngri\Downloads\Airplane'
rename_files_and_create_csv(base_directory_path)
