import os
names = os.listdir('movie_db/hidden_img')
for i in names:
    os.remove(f'movie_db/hidden_img/{i}')