import time
import sqlite3
import os
import file_scheduler
import pie_weighting_balance
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
strat_db_path = os.path.join(BASE_DIR, "strategies.db")
conn_strat = sqlite3.connect(strat_db_path, check_same_thread=False)
curs_strat = conn_strat.cursor()

strat_name=[row[0] for row in curs_strat.execute(f"SELECT strategy_name FROM strat").fetchall()]
freq=[row[0] for row in curs_strat.execute(f"SELECT frequency FROM strat").fetchall()]

while True:
    time.sleep(1)
    for x in range(len(strat_name)):

        file = open("memory/" + strat_name[x] + "_clock.txt", "r")
        try:
                current=file.read()
                print(current)
                file.close()
                if int(current)>=int(freq[x]) :
                        file_scheduler.run_file(strat_name[x])
                        pie_weighting_balance.main()
                        file = open("memory/" + strat_name[x] + "_clock.txt", "w")

                        file.write(str(0))
                else:
                        file = open("memory/" + strat_name[x] + "_clock.txt", "w")
                        file.write(str(int(current)+1))
                        file.close()
        except:
            file = open("memory/" + strat_name[x] + "_clock.txt", "w")

            file.write(str(0))

