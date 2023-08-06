"""The class that will store the aws access & secret keys for convenience"""

import boto3
import pandas as pd
import numpy as np
import pickle
from io import BytesIO
import json
import s3fs
from tensorflow.keras.models import load_model

class s3_connection():

    """The class that brings together all the s3 connection functions."""

    def __init__(self, aws_access_key, aws_secret_key):
        
        # Store the key variables in the class instance
        self.access_key = aws_access_key
        self.secret_key = aws_secret_key

        print(f"Stored the AWS Access Key & AWS Secret Key as variables in the class instance.")


    def read_csv_from_s3(self, bucket_name, object_name):

        """
        Read a csv file from s3 as a pandas DataFrame.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the data should be read from.

        object_name: str
            The path to the object within the bucket. eg "folder/subfolder/file.csv"
        
        Returns
        -------
        Pandas DataFrame object
        """

        # Create the s3fs client
        fs = s3fs.S3FileSystem(anon=False, key=self.access_key, secret=self.secret_key)

        # Open the file and read the csv through pandas
        data = pd.read_csv(fs.open(f"{bucket_name}/{object_name}", mode='rb'))

        return data


    def write_csv_to_s3(self, bucket_name, object_name, data):

        """
        Write a pandas DataFrame to a csv in s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the data should be written to.

        object_name: str
            The path to the object within the bucket. eg "folder/subfolder/file.csv"
        
        data: pandas.DataFrame
            The dataframe object to be saved to a csv.

        Returns
        -------
        None
        """

        # Connect to the S3 file system with the credentials
        fs = s3fs.S3FileSystem(anon=False, key=self.access_key, secret=self.secret_key)
        
        # Use 'w' for py3, 'wb' for py2
        with fs.open(f"{bucket_name}/{object_name}", "w") as f:
            data.to_csv(f, index=False)


    def read_npy_from_s3(self, bucket_name, object_name):

        """
        Read a list (.npy extension) from s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the file should be read from.

        object_name: str
            The path to the object within the bucket. eg "folder/subfolder/file.npy"

        Returns
        -------
        list
        """

        # Create the s3 boto3 rescource
        s3_resource = boto3.resource('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)

        # Read the npy file from the s3 bucket
        object = s3_resource.Object(bucket_name, object_name).get()['Body']

        # Convert the file type to Bytes and read it in
        with BytesIO(object.read()) as f:
            data = np.load(f, allow_pickle=True)

        return data


    def write_npy_to_s3(self, bucket_name, object_name, data):

        """
        Write a list to a .npy file in s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the data should be written to.

        object_name: str
            The path you want to write the list to within the bucket. eg "folder/subfolder/file.npy"
        
        data: list
            The list object to be saved to s3.

        Returns
        -------
        None
        """

        npy_buffer = BytesIO()
        
        pickle.dump(data, npy_buffer)

        # Create an s3 resource
        s3_resource = boto3.resource('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)

        # Put the object in the bucket
        s3_resource.Object(bucket_name, object_name).put(Body=npy_buffer.getvalue())


    def read_json_from_s3(self, bucket_name, object_name):

        """
        Read a json file from s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the data should be written to.

        object_name: str
            The path to the json file within the bucket. eg "folder/subfolder/file.json"

        Returns
        -------
        dict
        """

        # Create an s3 resource from boto3
        s3_resource = boto3.resource('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)

        # Get the object in s3
        obj = s3_resource.Object(bucket_name, object_name)

        # Extract the data from the s3 object
        data = json.load(obj.get()['Body']) 

        return data


    def write_h5_model_to_s3(self, model_object, bucket_name, object_name):

        """
        Write a keras model object (.h5 extension) to s3.
        
        Parameters
        ----------
        model_object: keras model object
            A trained keras model object.

        bucket_name: str
            The name of the bucket the data should be written to.

        object_name: str
            The path to the json file within the bucket. eg "folder/subfolder/file.json"
        
        Returns
        -------
        None
        """

        # First save the model to the local directory, to be copied to s3
        model_object.save(object_name)

        # Connect to s3 using s3fs
        s3 = s3fs.S3FileSystem(anon=False, key=self.access_key, secret=self.secret_key)

        # Put the model into s3
        s3.put(object_name, f"{bucket_name}/{object_name}")


    def read_h5_from_s3(self, bucket_name, object_name):

        """
        Read a h5 model object from s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the model object should be read from.

        object_name: str
            The path to the .h5 model object file within the bucket. eg "folder/subfolder/model_name.h5"
        
        Returns
        -------
        A keras model object
        """

        # Connect to s3 using s3fs
        s3 = s3fs.S3FileSystem(anon=False, key=self.access_key, secret=self.secret_key)

        # Copy the model object file to the local directory
        s3.get(f"{bucket_name}/{object_name}", object_name)

        # Read in the model that has been copied from s3
        model_object = load_model(object_name)

        return model_object


    def write_pkl_to_s3(self, pkl_object, bucket_name, object_name):

        """
        Write a pickled object (.pkl extension) to s3.
        
        Parameters
        ----------
        pkl_object: a pickled object
            A pickled object.

        bucket_name: str
            The name of the bucket the object should be written to.

        object_name: str
            The path to the json file within the bucket. eg "folder/subfolder/object.pkl"
        
        Returns
        -------
        None
        """

        # First save the model to the local directory, to be copied to s3
        pickle.dump(pkl_object, open(object_name, 'wb'))

        # Connect to s3 using s3fs
        s3 = s3fs.S3FileSystem(anon=False, key=self.access_key, secret=self.secret_key)

        # Put the model into s3
        s3.put(object_name, f"{bucket_name}/{object_name}")


    def read_pkl_from_s3(self, bucket_name, object_name):

        """
        Read a pickled object (.pkl extension) from s3.
        
        Parameters
        ----------
        bucket_name: str
            The name of the bucket the model object should be read from.

        object_name: str
            The path to the .h5 model object file within the bucket. eg "folder/subfolder/model_name.h5"
        
        Returns
        -------
        An unpickled object to be used
        """

        # Connect to s3 using s3fs
        s3 = s3fs.S3FileSystem(anon=False, key=self.access_key, secret=self.secret_key)

        # Copy the model object file to the local directory
        s3.get(f"{bucket_name}/{object_name}", object_name)

        # Read in the model that has been copied from s3
        pkl_object = pickle.load(open(object_name, 'rb'))

        return pkl_object