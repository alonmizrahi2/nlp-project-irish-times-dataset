import os
import time
import torch
import re
import datetime
import pandas as pd

# Walk into the path of data (find data in folder)
def path2data(args_config):
    for r, d, f in os.walk(args_config.data_root):
        req_data = [i for i in f if i.endswith("6.csv")]
    return os.path.join(r, req_data[0])

# Save the netowrk and is weights, if there is no folder open a new one.
def save_net(path, state):
    tt = str(time.asctime())
    img_name_save = 'net' + " " + str(re.sub('[:!@#$]', '_', tt))
    img_name_save = img_name_save.replace(' ', '_') + '.pt'
    _dir = os.path.abspath('../')
    path = os.path.join(_dir, path)
    t = datetime.datetime.now()
    datat = t.strftime('%m/%d/%Y').replace('/', '_')
    dir = os.path.join(path, 'net' + '_' + datat)
    if not os.path.exists(dir):
        try:
            os.makedirs(dir, exist_ok=True)
            print("Directory '%s' created successfully" % ('net' + '_' + datat))
        except OSError as error:
            print("Directory '%s' can not be created" % ('net' + '_' + datat))

    net_path = os.path.join(dir, img_name_save)
    print(net_path)
    torch.save(state, net_path)
    return net_path

def load_frompath(dir):
    # Expand the ~ shortcut to the full home directory path
    expanded_file_path = os.path.expanduser(dir)

    df = pd.read_csv(expanded_file_path)

    # Change the columns name (optional)
    df.rename(columns={'clean_headline_text': 'text', 'headline_category': 'category'}, inplace=True)
    df = df[['text', 'category']]  # Keep only 'text' and 'category' columns

    # Clean the data (optional, modify as per your requirements)
    df = df.dropna(subset=['text', 'category'])  # Remove rows with missing values in 'text' or 'category'
    df.drop_duplicates(inplace=True)
    return df
