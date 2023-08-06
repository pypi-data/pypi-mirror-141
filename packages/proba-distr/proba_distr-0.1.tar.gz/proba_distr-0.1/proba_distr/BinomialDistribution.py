import math
import matplotlib.pyplot as plt
from .GeneralDistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials
            
    """

    def __init__(self, prob=.5, size=20, mu=0, sigma=1):
        self.p = prob
        self.n = size
        self.mean = mu
        self.stdev = sigma
        Distribution.__init__(self, mu, sigma)
        
        
    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        self.mean = self.n * self.p

        return self.mean



    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
        self.stdev = math.sqrt(self.n * self.p * (1-self.p))

        return self.stdev
        
        
        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """        
        
        self.n = len(self.data)
        self.p = sum(self.data) / len(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()

        return self.p, self.n
                               
        
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
            
        fig, ax = plt.subplots()
        ax.hist(self.data)
        ax.set_title('Histogram of binomial distribution')
        ax.set_xlabel('data')                     
        ax.set_ylabel('count')
        plt.tight_layout()                               
        
                                             
                               
    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
                               
        a = (math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n-k)))
        b = (self.p ** k) * ((1-self.p) ** (self.n-k))
        pdf = a * b

        return pdf

                               

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        
        x = []
        y = []                       
        for i in range(0, self.n + 1):
            x.append(i)   
            y.append(self.pdf(i))    

        fig, ax = plt.subplots()
        ax.bar(x, y)
        ax.set_title('Distribution of outcomes')
        ax.set_xlabel('outcome')                     
        ax.set_ylabel('probability')
        plt.tight_layout()   

        return x, y                       
                               
                              
               
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        result.mean = self.calculate_mean()
        result.stdev = self.calculate_stdev()
                               
        return result
        
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
    
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)