import json
import psycopg2

try:
    # Substitua com suas próprias informações de conexão
    conn = psycopg2.connect(
    database="rickandmorty",
    user="rickandmorty_owner",
    password="r4oWfP8uFcJv",
    host="ep-calm-rice-a5vmq4zi.us-east-2.aws.neon.tech",
    port="5432"
)
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()

    # Se não houver exceções, a conexão foi bem-sucedida
    #print("Conexão bem-sucedida!")

    query = f"""
      CREATE TABLE IF NOT EXISTS characters (
        id SERIAL PRIMARY KEY,
        name VARCHAR(80),
        status VARCHAR(15),
        species VARCHAR(50),
        type VARCHAR(50),
        gender VARCHAR(15),
        origin_name VARCHAR(50),
        location_name VARCHAR(50),
        image_url VARCHAR(100)
      );
      """
    cursor.execute(query)

    conn.commit()

    with open("scripts/allCharsUpdated.json", encoding='utf-8') as file:
        data = json.load(file)

    #Organiza por id
    sorted_data = sorted(data, key=lambda x: x["id"])

    for item in sorted_data:
      print('id:', item['id'], ' Nome:', item['name'])
      query = f"""
      INSERT INTO characters (name, status, species, type, gender, origin_name, location_name, image_url)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
       """

      cursor.execute(query, (item["name"], item["status"], item["species"], item["type"], item["gender"], item["origin"]["name"], item["location"]["name"], item["image"]))

      conn.commit()


    cursor.close()

    conn.close()

except psycopg2.Error as e:
    print("Erro durante a conexão ao banco de dados:")
    print(e)