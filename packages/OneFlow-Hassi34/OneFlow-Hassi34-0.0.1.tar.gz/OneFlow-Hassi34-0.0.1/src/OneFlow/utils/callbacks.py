import tensorflow as tf
import time, os

def get_unique_filename(filename):
    unique_filename = time.strftime(f"%Y%m%d_%H%M%S_{filename}")
    return unique_filename
    

def get_callbacks (es_patience, callbacked_model_name ,model_ckpt_path):
    #Early stopping callback
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(patience=es_patience, restore_best_weights=True)
    #Model Checkpointing callback (Helpful in backup, would save the last checkpoint in crashing)
    CKPT_name = get_unique_filename(callbacked_model_name)
    CKPT_path = os.path.join( model_ckpt_path ,CKPT_name)
    checkpointing_cb = tf.keras.callbacks.ModelCheckpoint(CKPT_path , save_best_only=True)
    return early_stopping_cb, checkpointing_cb