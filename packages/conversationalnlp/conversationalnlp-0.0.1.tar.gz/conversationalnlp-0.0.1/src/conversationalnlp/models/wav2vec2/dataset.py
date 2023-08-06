import random
from IPython.display import display, HTML
from datasets import load_dataset
from datasets.dataset_dict import DatasetDict
from transformers import Wav2Vec2Processor
import soundfile as sf
import pandas as pd
import logging
import re
import os
import json

class Wav2Vec2Dataset:
    """
    Long input sequences require a lot of memory. 
    Since Wav2Vec2 is based on self-attention the memory requirement scales quadratically with the input length for long input sequences
    TODO: remove rows with audio length > n seconds/word count > n

    """

    chars_to_ignore_regex = '[\,\?\.\!\-\;\:\"]'

    def __init__(self):
        pass

    def loadHFdataset(self, dataset : DatasetDict):
        """
        Attributes
        ----------
        dataset : datasets.dataset_dict.DatasetDict
            In house dataset hosted on Hugging face hub
        """

        self.dataset = self._normalizetext(dataset)
        self.show_random_elements(self.dataset["train"])

    def loadcustomdataset(self, datadict : dict):
        """
        Attributes
        ----------
        datadict : dict
        
            dict with keys "train" and "test", both stating absolute csv file paths
        """
        rawdataset = load_dataset("csv", data_files=datadict)
        self.show_random_elements(rawdataset["train"])

        self.dataset = self._normalizetext(rawdataset)
        self.show_random_elements(self.dataset["train"])

    def _prepare_dataset(self, batch):
        """
        - Process the dataset to the format expected by the model for training
        - Use map(...) function
        1. Load and resample the audio data, simply by calling batch['audio']
        2. Extract the input_values from the loaded audio file (In our case, the Wav2Vec2Processor only normalized the data)
        3. Encode the transcriptions to label ids
        """
        if(os.path.exists(batch['file']) != True):
        
            logging.info(f"{batch['file']} not available")
            
        audio, samplerate = sf.read(batch['file'])    
        # batched output is "un-batched" to ensure mapping is correct
        batch["input_values"] = self.processor(audio, sampling_rate=samplerate).input_values[0]
        
        with self.processor.as_target_processor():
            batch["labels"] = self.processor(batch["text"]).input_ids

        return batch

    def vectorize(self, processor : Wav2Vec2Processor) -> DatasetDict:
        """
        Prepare dataset with def prepare_dataset

        Returns
        -------
        datasets.dataset_dict.DatasetDict
        """
        self.processor = processor

        dataset = self.dataset.map(self._prepare_dataset, remove_columns=self.dataset.column_names["train"])#, num_proc=4)
        
        del self.dataset

        return dataset

    def _normalizetext(self, dataset : DatasetDict) -> DatasetDict:
        """
        Normalize text 

        Returns
        -------
        datasets.dataset_dict.DatasetDict
        
        """
        logging.info("Normalize text")
        return dataset.map(self._remove_special_characters)

    def _remove_special_characters(self, batch):
        """
        Remove special characters from transcriptions and normalized them to lower-case only
        """
        batch["text"] = re.sub(self.chars_to_ignore_regex, '', batch["text"]).lower()
        return batch

    """
    def _setvocabpath(self, datadict):

        filename = datadict['train'].split(os.sep)[-1]
        vocabfolderpath = datadict['train'][0: -len(filename)- 1]
        self.vocababspath = os.path.join(vocabfolderpath, "vocab.json")
    """

    def buildvocabulary(self, vocabpath : str, vocabfilename = "vocab.json") -> str:
        """
        Build vocabulary from all the unique characters

        Attributes
        ----------
        vocabpath : str
            Path to save vocabulary file
        vocabfilename : str, optional
            File name of vocabulary file

        Returns
        -------
        vocababspath : str
            absolute path of vocabulary file         
        """
        logging.info("Build vocabulary from all unique characters")

        vocabs = self.dataset.map(self._extract_all_chars, batched=True, batch_size=-1, keep_in_memory=True, remove_columns=self.dataset.column_names["train"])

        vocab_list = list(set(vocabs["train"]["vocab"][0]) | set(vocabs["test"]["vocab"][0]))
        vocab_dict = {v: k for k, v in enumerate(vocab_list)}

        #space (" ") has its own token class, replace with more visible character 
        vocab_dict["|"] = vocab_dict[" "]
        del vocab_dict[" "]

        #add an "unknown" token so that model can later deal with characters not encountered
        vocab_dict["[UNK]"] = len(vocab_dict)

        #Add padding token that corresponds to CTC's "blank token"
        #The "blank token" is a core component of the CTC algorithm
        vocab_dict["[PAD]"] = len(vocab_dict)
        
        logging.info(f"Vocabulary size: {len(vocab_dict)}")
        logging.info(f"The pretrained Wav2Vec2 checkpoint will have an output dimension of {len(vocab_dict)}")

        vocababspath = os.path.join(vocabpath, vocabfilename)

        with open(vocababspath, 'w') as vocabfile:
            json.dump(vocab_dict, vocabfile)


        return vocababspath

    def _extract_all_chars(self, batch):
        """
        Process input string to get unique characters
        """
        all_text = " ".join(batch["text"])
        vocab = list(set(all_text))
        return {"vocab": [vocab], "all_text": [all_text]}

    def show_random_elements(self, dataset, num_examples=1):
        assert num_examples <= len(dataset), "Can't pick more elements than there are in the dataset."
        picks = []
        for _ in range(num_examples):
            pick = random.randint(0, len(dataset)-1)
            while pick in picks:
                pick = random.randint(0, len(dataset)-1)
            picks.append(pick)
        
        df = pd.DataFrame(dataset[picks])
        display(HTML(df.to_html()))

