import pandas as pd
import pkg_resources

class GenderizerQc:
    """Class to evaluate the gender of a person based on his first name. 
    Data used to make the prediction are 200k boys and 200k girls born between 1980-2020 in Quebec.

    Keep in mind that the prediction might not be very good for names of person born before 1980 or after 2020.
    """
    def __init__(self):
        """
        Instance of the genderizerQc. It contains the data used to make the prediction. Only one instance is necessary
        """
        streamG =pkg_resources.resource_stream(__name__, '/data/gars1980-2020.csv')
        streamF =pkg_resources.resource_stream(__name__, '/data/filles1980-2020.csv')
        self.__dfG = pd.read_csv(streamG, index_col=0, skiprows=4)
        self.__dfF = pd.read_csv(streamF, index_col=0, skiprows=4)

    def __getCountG(self, name:str) -> int:
        """returns the number of boys with that name

        Args:
            name (str): first name to get the count of

        Returns:
            int: 0 if None found else the number of boys in Quebec with that name between 1980 and 2020
        """
        try:
            count = self.__dfG["Total"].loc[name.upper()]
        except KeyError:
            count = 0
        return count
    
    def __getCountF(self, name:str)->int:
        """returns the number of girls with that name

        Args:
            name (str): first name to get the count of

        Returns:
            int: 0 if None found else the number of girls in Quebec with that name between 1980 and 2020
        """
        try:
            count = self.__dfF["Total"].loc[name.upper()]
        except KeyError:
            count = 0
        return count
    
    def __evaluate(self, name:str)-> tuple:
        """Evaluates the probability of the gender given the number of boys and girls found with that same name.
        
        The formula is simply : probB_name = countB/(countB + countF)

        The is the probability of a name being a boy given the count. If the value is over 0.5, we return 1-probB_name and indicates that it is a girl.

        Args:
            name (str): name of the person to infer the gender

        Returns:
            _type_: _description_
        """
        gender, prob, total = None, 0, 0
        countB = self.__getCountG(name)
        countF = self.__getCountF(name)
        try:
            probB_name = countB/(countB + countF)
        except ZeroDivisionError:
            probB_name = 0
            
        if probB_name == 0:
            return gender, prob, total
        if probB_name > 0.5:
            gender = 'male'
            prob = probB_name
            total = countB + countF
        else:
            gender = 'female'
            prob = 1-probB_name
            total = countB + countF
            
        return gender, prob, total
    
    def __genderize(self, name:str)->dict:
        """Returns a dictionnary with the name, gender, probablity, count and country_id for 
        one name. This response has the same format as genderize.io's API. 

        If the name wasn't found in the data, the default value are returned with gender as None.

        Default return values are gender = None, probability=0, count=0, country_id = 'Qc'


        Args:
            name (str): first name to predict the gender.

        Returns:
            dict: json like object with name, gender, probability, count, country_id.
        """
        _name = name
        gender = None
        probability = 0
        count = 0
        country_id = 'Qc'
        gender, probability, count = self.__evaluate(name)
        return {
            "name":_name,
            "gender": gender,
            "probability": probability,
            "count":count,
            "country_id":country_id
        }
    def genderize(self, listName:list)-> list:
        """Evaluates a list of names and returns a list of json like object countaining the same format as genderize.io's API.

        If the name wasn't found in the data, the default value are returned with gender as None.

        Default return values are gender = None, probability=0, count=0, country_id = 'Qc'

        Args:
            listName (list[str]]): list of name to infer the gender

        Returns:
            list[dict]: list of json like object with name, gender, probability, count, country_id.
        """
        results = []
        for name in listName:
            results.append(self.__genderize(name))
        return results
    