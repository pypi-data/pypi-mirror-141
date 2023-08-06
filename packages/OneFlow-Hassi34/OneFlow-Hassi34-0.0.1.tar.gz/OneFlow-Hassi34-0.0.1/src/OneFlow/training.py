from matplotlib.pyplot import hist
from utils.common import read_config 
from utils.data_mgmt import get_data
from utils.callbacks import get_callbacks
from utils.model import create_model, save_model, save_plot
import argparse, os 

def training(config_path):
    config = read_config(config_path)
    validation_datasize = config["params"]["validation_datasize"]
    (X_train, y_train), (X_valid, y_valid), (X_test, y_test) = get_data(validation_datasize)
    
    LOSS_FUNCTION = config["params"]["loss_function"]
    OPTIMIZER = config['params']['optimizer']
    METRICS = config["params"]["metrics"]
    NUM_CLASSES = config["params"]["num_classes"]
    model = create_model(LOSS_FUNCTION, OPTIMIZER, METRICS, NUM_CLASSES) #returns untrained model

    EPOCHS = config['params']["epochs"]
    VALIDATION_SET = (X_valid, y_valid) 
    ES_PATIENCE = config['params']['es_patience']
    model_ckpt_dir = config['artifacts']['model_ckpt_dir']
    artifacts_dir = config["artifacts"]["artifacts_dir"]
    model_dir = config["artifacts"]["model_dir"]
    model_ckpt_path = os.path.join(artifacts_dir,model_dir, model_ckpt_dir)
    os.makedirs(model_ckpt_path, exist_ok=True)
    callbacked_model_name = config['artifacts']['callbacked_model_name']
    early_stopping_cb, checkpointing_cb = get_callbacks(ES_PATIENCE, callbacked_model_name, model_ckpt_path)
    history = model.fit(X_train, y_train, epochs=EPOCHS, validation_data = VALIDATION_SET, callbacks = [early_stopping_cb, checkpointing_cb])

    
    model_dir = config["artifacts"]["model_dir"]

    model_dir_path = os.path.join(artifacts_dir,model_dir)
    os.makedirs(model_dir_path, exist_ok = True)
    model_name = config['artifacts']['model_name']
    save_model(model, model_name, model_dir_path)
    
    plots_dir = config["artifacts"]["plots_dir"]
    plots_dir_path = os.path.join(artifacts_dir, plots_dir )
    os.makedirs(plots_dir_path, exist_ok=True)
    plot_name = config["artifacts"]["plot_name"]
    save_plot(history, plot_name, plots_dir_path)



if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-c", "--config", default="config.yaml")

    parsed_args = args.parse_args()
    training(config_path = parsed_args.config)