import requests
with open("dependencies.txt", "r") as f:
    dependencies = f.readlines()

base_url = "https://repo1.maven.org/maven2/"
for s in dependencies:
    s = s.strip()
    group_id, artifact_id = s.split("#")
    artifact_id, version = artifact_id.split(";")
    version = version.split(" ")[0]
    group_id = group_id.replace(".", "/")
    url = f"{base_url}{group_id}/{artifact_id}/{version}/{artifact_id}-{version}.jar"
    print("Downloading: ", url)
    # Download the file
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Save the file to disk
        with open(f"jars/{artifact_id}-{version}.jar", "wb") as f:
            f.write(response.content)
        print(f"Downloaded {artifact_id}-{version}.jar")
    else:
        raise Exception(f"Failed to download {artifact_id}-{version}.jar: {response.status_code}")
    
for s in dependencies:
    s = s.strip()
    _, artifact_id = s.split("#")
    artifact_id, version = artifact_id.split(";")
    version = version.split(" ")[0]
    print(f"/home/spark/jars/{artifact_id}-{version}.jar", end=",")

print()