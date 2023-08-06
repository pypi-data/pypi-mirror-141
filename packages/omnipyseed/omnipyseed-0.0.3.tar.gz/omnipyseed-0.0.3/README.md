# omnipyseed
Omnipyseed is a minimal Python package that seeds all the basic Random Number
Generators (RNGs) in a Python script. The purpose of omnipyseed is to simplify
the process of seeding numerical simulations which use packages such as 
Numpy and Pytorch.


## Dependencies

**omnipyseed** does not depend on any non-essential Python package.


## Installation

You can install **omnipyseed** using pip:
```
pip3 (or pip) install omnipyseed
```
Or you can clone this repository to any of your local directories and install
it from there.
```
$ git clone https://github.com/gdetor/omnipyseed.git
$ cd omnipyseed/
$ pip install .
```

## How to use

```
import numpy as np
from omnipyseed import seeding      # import the seeding module from omnipyseed


if __name__ == '__main__':
    seeding.universal_seed(13)      # call the universal_seed function to seed
                                    # Python and Numpy
    x = np.linspace(-1, 1, 10)
    y = np.sin(2*np.pi*5*x)
    print(y)
```

## Caveat

Please do not use **omnipyseed** if you'd like to use different random states
for different random parts of your project. Instead you should instantiate 
generator objects with a seed and pass it around (*e.g.*, 
numpy.random.default_rng(*seed*)). 
