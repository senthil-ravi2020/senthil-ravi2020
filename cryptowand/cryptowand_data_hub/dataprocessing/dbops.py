import psycopg2
import json
import os
import yaml
# establishing the connection

basedir = os.getcwd()
with open(basedir + '/config/cryptowand_config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

database_name = config['storage']['database']['name']
database_user = config['storage']['database']['user']
database_password = config['storage']['database']['password']
database_host = config['storage']['database']['host']
database_port= config['storage']['database']['port']

def insert_cw_json_todb(json_all_coins):
    try:
        conn = psycopg2.connect(
            database=database_name, user=database_user, password=database_password, host=database_host, port=database_port
        )
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Executing an MYSQL function using the execute() method

        for key in json_all_coins:
            postgres_insert_query = """ INSERT INTO cw_pricing_snapshot 
            (
                batch_id,
                coin_symbol,
                rank,
                pct_change_prev_run,
                coin_img_url,
                coin_slug,
                coin_name,
                coin_details_url,
                coin_position_moves,
                price,
                twitter_followers,
                github_stars,
                reddit_posts_perday,
                cryptothermo_pct_1h,
                cryptothermo_pct_24h,
                cryptothermo_pct_7d,
                cryptothermo_pct_30d,
                cryptothermo_bit1,
                cryptothermo_bit2,
                cryptothermo_bit3,
                cryptothermo_bit4,
                whale_sentiment,
                onchain_sentiment,
                current_marketcap,
                marketcap_dominance  
                ) 
            VALUES (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s, 
                %s,%s,%s,%s,%s, 
                %s,%s,%s,%s,%s, 
                %s,%s,%s,%s,%s
            ) """
            
            record_to_insert = (
                json_all_coins[key]['batch_id'],
                json_all_coins[key]['coin_symbol'],
                json_all_coins[key]['rank'],
                json_all_coins[key]['pct_change_prev_run'],
                json_all_coins[key]['coin_img_url'],
                json_all_coins[key]['coin_slug'],
                json_all_coins[key]['coin_name'],
                json_all_coins[key]['coin_details_url'],
                json_all_coins[key]['coin_position_moves'],
                json_all_coins[key]['price'],
                json_all_coins[key]['twitter_followers'],
                json_all_coins[key]['github_stars'],
                json_all_coins[key]['reddit_posts_perday'],
                json_all_coins[key]['cryptothermo_pct_1h'],
                json_all_coins[key]['cryptothermo_pct_24h'],
                json_all_coins[key]['cryptothermo_pct_7d'],
                json_all_coins[key]['cryptothermo_pct_30d'],
                json_all_coins[key]['cryptothermo_bit1'],
                json_all_coins[key]['cryptothermo_bit2'],
                json_all_coins[key]['cryptothermo_bit3'],
                json_all_coins[key]['cryptothermo_bit4'],
                json_all_coins[key]['whale_sentiment'],
                json_all_coins[key]['onchain_sentiment'],
                json_all_coins[key]['current_marketcap'],
                json_all_coins[key]['marketcap_dominance']
            )
        
            cursor.execute(postgres_insert_query, record_to_insert)
            conn.commit()

        # Fetch a single row using fetchone() method.

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into cw_pricing_snapshot table", error)

    # Closing the connection
    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def read_json(json_all_coins):

    for key in json_all_coins:
        print(json_all_coins[key]['coin_position_moves'])

    return
