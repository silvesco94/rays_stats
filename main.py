import csv 
from flask import Flask, request, render_template

app = Flask(__name__)
DATAFILE = 'data.csv'
FIELDNAMES = ['id','name','avg','hr', 'war']

rays_stats = []

def load_data_file(): 
  with open('data.csv') as data_file: 
    reader = csv.DictReader(data_file)
    for row in reader: 
      rays_stats.append(row)
      
def append_data_file(new_row):
  with open(DATAFILE, 'a', newline='') as data_file:
    writer = csv.DictWriter(data_file, FIELDNAMES)
    writer.writerow(new_row)

def dump_data_file():
  with open(DATAFILE, 'w', newline='') as data_file:
    writer = csv.DictWriter(data_file, FIELDNAMES)
    writer.writeheader()
    for stat in rays_stats:
      writer.writerow(stat)

@app.route('/rays_stats')
def rays_stats_index():
  return render_template('index.html', rays_stats=rays_stats)

@app.route('/rays_stats/<id>')
def get_ray_stat(id):
  # Use the id to look up the proper stat from the rays_stats list!
  for stat in rays_stats:
    if stat['id'] == id:

      return render_template('show.html', stat=stat)
      # return stat
  return {'error' : 'not found'} , 404 

@app.route('/rays_stats', methods = ['POST'])
def create_ray_stat():
  # 1 get stat info from user
  new_stat = request.get_json()
  #2 append it to rays_stats list
  rays_stats.append(new_stat)
  
  append_data_file(new_stat)
  #3 acknowledge that it was successful 
  return {'message': 'Stat created successfully!'}, 201 


@app.route('/rays_stats/<id>', methods = ['PATCH'])
def rays_stats_update(id):
  #1 get updated movie info from user 
  updated_stat= request.get_json()
  print(updated_stat)
  #2 look in list of movies for matching movies and update it
  for stat in rays_stats: 
    if stat['id'] == id: 
      stat.update(updated_stat)
      dump_data_file()
      return {'message' : 'Stat updated successfully!'}, 201
  #3 acknowledge that it was successful OR not found
  return {'error' : 'Not Found'}, 404

@app.route('/rays_stats/<id>', methods=['DELETE'])
def movies_delete(id):
  # 1 - Find the index corresponding to the id the user supplied
  found_idx = None

  # 2 - Using that index, pop from the movies list
  for i in range(len(rays_stats)):
    if rays_stats[i]['id'] == id:
      found_idx = i
      break

  if found_idx != None:
    rays_stats.pop(found_idx)

    # 3 - Remove it from the CSV file
    dump_data_file()
    
    return { 'message': 'Stat deleted successfully!' }, 201
  return { 'error': 'Not Found' }, 404


load_data_file()
print(rays_stats)
app.run(host='0.0.0.0')
# Copy your Part 2's main.py here to start!
