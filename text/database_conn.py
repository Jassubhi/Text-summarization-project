import psycopg2

conn = psycopg2.connect(database="dbrolo3n8dbgrp", user="udqhymlpwxvcbb",
                        password="f877f7ebc264d2771e60f278adca0bc266d0323a3a319134b93fce964c805766",
                        host="ec2-54-236-146-234.compute-1.amazonaws.com",
                        port="5432")

print("Opened database successfully")


cur = conn.cursor()

cur.execute("""
    Delete from upload_document where username_id IS null;
    """)


print("Updated successfully")

conn.commit()
conn.close()





