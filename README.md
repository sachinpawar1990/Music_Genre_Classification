# Music_Genre_Classification

This directory contains following files:
1. Dockerfile - This is the file which is needed to create a Docker image in the new system
2. requirements.txt - This is the file which has all the Python packages with the versions. This is needed while building the Docker Image.

Steps for the Deployment:
1. First download this file structure in the zipped format or clone the directory.
2. If zipped format is chosen, unzip it.
3. Go to command prompt and change directory to this path where above directory is zipped/cloned.
4. Ensure system has Docker Desktop (for Windows) or any other docker application.
5. Ensure that this system has stable internet connectivity.
6. Execute "docker build --tag python_imgdbs ." command in the command prompt. It would build a Docker Image by getting packages from internet.
7. Once succesful, ensure that docker image is created by executing "docker images" in the command prompt.
8. Run the Genre Prediction job by running following command in the command prompt:
"docker run -it --rm -v Path_of_your_local_system_of_folder_Music_Genre_Classification\app\input_data:/app/input_data -v Path_of_your_local_system_of_folder_Music_Genre_Classification\app\output_data:/app/output_data -v Path_of_your_local_system_of_folder_Music_Genre_Classification\app:/app -p 8000:8000 python_imgdbs". Replace "Path_of_your_local_system_of_folder_Music_Genre_Classification" with the path of your system where this directory is present after downloading.
9. If it shows the message "Uvicorn running on http://127.0.0.1:8000", then it is successful.
10. It would first generate the result in the output_data folder.
11. App could be accessed by going on "http://127.0.0.1:8000/".
12. There are 3 API requests which could be made:
  i. upload_classified_results - Accessed by http://127.0.0.1:8000/upload_classified_results. This puts the results into the SQLite database, so it should be executed first.
  ii. get_all_genres - Accessed by http://127.0.0.1:8000/get_all_genres. It gets all the genres present in the database along with the titles of the genres.
  iii. get_title_from_genre - Accessed by http://127.0.0.1:8000/get_title_from_genre?genre=genre_name. It gives all the titles present in the database when provided with certain genre name. Here, genre name should be provided. So, for genre "folk", link would be http://127.0.0.1:8000/get_title_from_genre?genre=folk
