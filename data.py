import pandas as pd 
import numpy as np

price_var = 'princ' # variable that must be in cars: cars['pr']/(cars['ngdp']/cars['pop'])

def get_x_y(cars, dummyvarlist = ['brd'], 
            control_vars = ['home', 'cy', 'hp', 'we', 'li'],
            STANDARDIZE_X = False, ADD_HOME_MARKET_PRICE_INTERACTION = False,
            I = None):
    '''
    Inputs:
        cars: dataframe
        price_var: string, name of price variable
        dummyvarlist: list of strings, names of dummy variables
        controls: list of strings, names of control variables
        STANDARDIZE_X: boolean, whether to standardize X
        I: vector of booleans
    Outputs:
        x: numpy array, shape (N,J,K)
    '''

    M = cars.ma.nunique()
    T = cars.ye.nunique()
    N = M*T
    J = cars.shape[0]/N 
    assert J == int(J), 'Number of rows is not an integer multiple of N'
    J = int(J)

    # log transform the price variable 
    DOLOGP = False # use the non-logarithmic measure of price (i.e. price relative to income)
    if DOLOGP: 
        controls = ['logp'] + control_vars
        cars['logp'] = np.log(cars[price_var])
    else: 
        controls = ['p'] + control_vars
        cars['p'] = cars[price_var]

    if ADD_HOME_MARKET_PRICE_INTERACTION: 
        # new variable: price elasticity heterogeneous for home-region 
        cars['logp_x_home'] = cars[price_var] * cars['home']
        controls += ['logp_x_home']

    x_vars = []
    
    x_controls = cars[controls].values
    if STANDARDIZE_X:
        x_controls = ((x_controls - x_controls.mean(0))/(x_controls.std(0)))

    x_vars += controls 
    x = x_controls.copy()

    if dummyvarlist is not None: 
        for dummyvar in dummyvarlist: 
            dummies = pd.get_dummies(cars[dummyvar])
            dummy_names = [f'{dummyvar}={v}' for v in list(dummies.columns[1:].values)] # omit a reference category 
            x_dummies = dummies.values[:, 1:]
            x_vars += dummy_names
            x = np.hstack([x.reshape(N*J,-1), x_dummies]).reshape(N,J,-1)
    else:
        dummy_names = []
        x_dummies = []
        x = x_controls.reshape(N,J,-1)
        
    K = len(x_vars)
    print(f'K = {K} variables selected.')
    
    y = cars['s'].values.reshape(N,J)
    
    return x,y,x_vars

def set_price_var_in_x_for_car_j(x:np.ndarray, p:float, j:int, cars:pd.DataFrame) -> np.ndarray:
    assert cars['ye'].nunique()==1, 'Only works for one year'
    assert cars['ma'].nunique()==1, 'Only works for one market'

    # These should be unique 
    assert cars['pop'].nunique()==1, 'population not unique'
    assert cars['inc'].nunique()==1, 'national not unique'
    pop = cars['pop'].unique()[0]
    inc = cars['inc'].unique()[0]
    
    
    return False
