
import numpy as np
import pandas as pd
import scipy
import os
import sys
from scipy.stats import norm
from colorama import Fore, Back, Style
# print(Fore.RED+ 'done import packages' + Style.RESET_ALL)
def add_(x,y):
    return x+y
'''
To do:
>Propotion Metrics:
    + sample size N=2 : (v)
    + pvalue (v)
    + power calculation (v)

> Volume Metrics:
    + sample size : checking
    + power calculation (v)
    + P value calculation (v)

> Ratio Metrics:

    
    
> Others:
    + check the sample size formula for multivariate testing A/B/n
    
    + add proportional Chisquare testing
   
    + Futility boundary for sequential testin
    
'''


def calc_sample_size(N=2,p=.5,ci=.05,power=.8,mde=.25,one_sided=False,Bonf_correction=False):
    '''Check the condition here'''
    check_condition=True
    if N <=1 or N!=round(N,0):
        print('please check number of testing N again, it should be an interger in (2,20), defaul value 2')
        check_condition=False
        return np.NaN, np.NaN, np.NaN
    
    if ci <=0 or ci>=1:
        print('please check confidence level ci again, it should be in (0,1), defaul value .05')
        check_condition=False
        return np.NaN, np.NaN, np.NaN

    if power <=0 or power>=1:
        print('please check power level again, it should be in (0,1), defaul value .8')
        check_condition=False
        return np.NaN, np.NaN, np.NaN
    if mde <=0 or mde+p>=1:
        print(f'please check mde level again, it should be in (0%, {100*(1-p)}%), default value 25%')
        check_condition=False
        return np.NaN, np.NaN, np.NaN

    if p <=0 or p>=1:
        print('please check baseline rate again, it should be in (0,1), defaul value .5')
        check_condition=False
        return np.NaN, np.NaN, np.NaN

    if one_sided== True :
        # print('sone sided test')
        if Bonf_correction==True:
        
            t_alpha2=abs(norm.ppf(ci/((N-1))))
        else:
            t_alpha2=abs(norm.ppf(ci/((2-1))))
            
    else: 
        if Bonf_correction==True:
            t_alpha2=abs(norm.ppf(ci/(2*(N-1))))
        else:
            t_alpha2=abs(norm.ppf(ci/(2*(2-1))))
            
    
    t_beta=abs(norm.ppf(power))
    # print(t_alpha2)
    # print(t_beta)
    '''Estimate pool variance '''
    # pool_var=p*(1-p)
    pool_var=(p*(1-p)+(p+mde)*(1-p-mde))/2
    # test 
    # t_alpha2=1.96
#         t_beta=.84
    
    N_min=2*pool_var*pow((t_alpha2+t_beta),2)/pow(mde,2)
    
    base_lift=mde/p
    base_cohen_D=mde/(pow(pool_var,.5))

    
    return [round(N_min,0),round(base_lift,2), round(base_cohen_D,2)]

def calc_sample_size_vol_2(N=2,sum_volume=295000,sum_square_vol=250000000, number_of_visitor=18000,ci=.05,power=.8,mde=1.64,one_sided=False,Bonf_correction=False):
    '''Check the condition here'''
    check_condition=True
    try:
        sum_volume=float(sum_volume)
        sum_square_vol=float(sum_square_vol)
        number_of_visitor=float(number_of_visitor)
        N=float(N)
        ci=float(ci)
        power=float(power)
        mde=float(mde)
    except:
        print('Invalid Input...')
        check_condition=False
        return np.NaN, np.NaN, np.NaN
        
        
        
    if N <=1 or N!=round(N,0):
        print('please check number of testing N again, it should be an interger in (2,20), defaul value 2')
        check_condition=False
        return np.NaN, np.NaN, np.NaN

    if ci <=0 or ci>=1:
        print('please check confidence level ci again, it should be in (0,1), defaul value .05')
        check_condition=False
        return np.NaN, np.NaN, np.NaN
    if mde <=0 :
        print('please check mde level again, it should be positive value, default value .5')
        check_condition=False
        return np.NaN, np.NaN, np.NaN

    if power <=0 or power>=1:
        print('please check power level again, it should be in (0,1), defaul value .8')
        check_condition=False
        return np.NaN, np.NaN, np.NaN
    
    if sum_volume <=0 or sum_square_vol<=0 or number_of_visitor <=0:
        print('Invalid input ')
        check_condition=False
        return np.NaN, np.NaN, np.NaN
    
    if one_sided== True:
        # print('sone sided test')
        t_alpha2=abs(norm.ppf(ci/((N-1))))
    else:    
        t_alpha2=abs(norm.ppf(ci/(2*(N-1))))

    mean_based=sum_volume/number_of_visitor
    sigma_based=pow((sum_square_vol-number_of_visitor*pow(mean_based,2))/(number_of_visitor-1),.5)

    pool_var=(sum_square_vol-number_of_visitor*pow(mean_based,2))/(number_of_visitor-1)

    if pool_var <=0 :
        print(' invalid input for total volumne, and total square volume')
        check_condition=False
        return np.NaN, np.NaN, np.NaN
    
    if check_condition ==True:
        t_beta=abs(norm.ppf(power))
        # print(t_alpha2)
        # print(t_beta)
        '''Estimate pool variance '''
        # print('mean based',sum_volume,number_of_visitor)
        
        # print('mean based',round(mean_based,4))
        
        # print(sigma_based,pool_var)


        N_min=2*pool_var*pow((t_alpha2+t_beta),2)/pow(mde,2)

        base_lift=mde/mean_based
        base_cohen_D=mde/(pow(pool_var,.5))


        return [round(N_min,0),round(base_lift,2), round(base_cohen_D,2)]

def calc_sample_size_vol(N=2,sigma_based=50,ci=.05,power=.8,mde=10,one_sided=False,Bonf_correction=False):
    '''Check the condition here'''
    check_condition=True
    if N <=1 or N!=round(N,0):
        print('please check number of testing N again, it should be an interger in (2,20), defaul value 2')
        check_condition=False
        return np.NaN, np.NaN, np.NaN

    if ci <=0 or ci>=1:
        print('please check confidence level ci again, it should be in (0,1), defaul value .05')
        check_condition=False
        return np.NaN, np.NaN, np.NaN

    if power <=0 or power>=1:
        print('please check power level again, it should be in (0,1), defaul value .8')
        check_condition=False
        return np.NaN, np.NaN, np.NaN

    if one_sided== True:
        # print('one sided test')
        t_alpha2=abs(norm.ppf(ci/((N-1))))
    else:    
        t_alpha2=abs(norm.ppf(ci/(2*(N-1))))

    t_beta=abs(norm.ppf(power))
    # print(t_alpha2)
    # print(t_beta)
    '''Estimate pool variance '''
    pool_var=pow(sigma_based,2)

    N_min=2*pool_var*pow((t_alpha2+t_beta),2)/pow(mde,2)

    base_lift=0 # need tp change
    base_cohen_D=mde/(pow(pool_var,.5))


    return [round(N_min,0),round(base_lift,2), round(base_cohen_D,2)]

def calc_power(group1_size,group2_size,group1_mean,group2_mean,alpha_level = 0.05, alternative='two-sided'):
    from statsmodels.stats.power import TTestIndPower


    n1 = group1_size       # number of observations of sample 1
    n2 = group2_size       # number of observations of sample 2
    sigma1=np.sqrt(group1_mean*(1-group1_mean))
    sigma2=np.sqrt(group2_mean*(1-group2_mean))
    s_pooled2 = np.sqrt(((n1 - 1)*sigma1**2 + (n2 - 1)*sigma2**2)/(n1 + n2 - 2))

    effect_size = (group1_mean - group2_mean)/s_pooled2
    ratio = n2/n1

    power_out = TTestIndPower().solve_power(effect_size = effect_size,
                                        power = None,
                                        nobs1 = n1,
                                        ratio = ratio,
                                        alpha = alpha_level,
                                        alternative = alternative)
    # print(power_out)
    return power_out


def calc_power_volume(group1_size,group2_size,group1_mean,group2_mean,sigma1,sigma2,alpha_level = 0.05,alternative='two-sided'):
    from statsmodels.stats.power import TTestIndPower


    n1 = group1_size       # number of observations of sample 1
    n2 = group2_size       # number of observations of sample 2
    s_pooled2 = np.sqrt(((n1 - 1)*sigma1**2 + (n2 - 1)*sigma2**2)/(n1 + n2 - 2))

    effect_size = (group1_mean - group2_mean)/s_pooled2
    ratio = n2/n1

    power_out = TTestIndPower().solve_power(effect_size = effect_size,
                                        power = None,
                                        nobs1 = n1,
                                        ratio = ratio,
                                        alpha = alpha_level,
                                        alternative = alternative)
    # print(power_out)
    return power_out

def calc_p_val_vol(group1_size,group2_size,group1_mean,group2_mean,sigma1,sigma2,alpha_level,one_sided_test=False):
    from statsmodels.stats.power import TTestIndPower


    n1 = group1_size       # number of observations of sample 1
    n2 = group2_size       # number of observations of sample 2
    s_pooled2 = np.sqrt(pow(sigma1,2)/n1 + pow(sigma2,2)/n2)
    q=(group2_mean-group1_mean)/s_pooled2
    # print('statistic :', q)
    if one_sided_test== False:
        p_val=scipy.stats.norm.sf(abs(q))*2
        # print('p_value: ',p_val)
        critical_val=norm.ppf(1-alpha_level/2)*s_pooled2
        # print('critical value:',critical_val)
    else:   
        p_val=scipy.stats.norm.sf(abs(q))
        # print('p_value: ',p_val)
        critical_val=norm.ppf(1-alpha_level)*s_pooled2
        # print('critical value:',critical_val)

    return p_val, critical_val,q
def calc_p_val_prop(group1_size,group2_size,p1,p2,alpha_level,one_sided_test=False):
    from statsmodels.stats.power import TTestIndPower


    n1 = group1_size       # number of observations of sample 1
    n2 = group2_size       # number of observations of sample 2
    s_pooled2 = np.sqrt(p1*(1-p1)/n1 +p2*(1-p2)/n2)

    q=(p2-p1)/s_pooled2

    # print('statistic :', q)
    if one_sided_test== False:
        p_val=scipy.stats.norm.sf(abs(q))*2
        # print('p_value: ',p_val)
        critical_val=norm.ppf(1-alpha_level/2)*s_pooled2
        # print('critical value:',critical_val)
    else:   
        p_val=scipy.stats.norm.sf(abs(q))
        # print('p_value: ',p_val)
        critical_val=norm.ppf(1-alpha_level)*s_pooled2
        # print('critical value:',critical_val)

    return p_val, critical_val,q

def get_Nmin(metric_type, message=True, plot=True):
    # print('Calculating Nmin...')
    if metric_type=='Binary metric':
        print('Calculating Nmin...')
    
        N_groups=Number_Of_Groups_box.value
        conf_level=conf_level_box.value/100
        alpha_level=round(1-conf_level,2)
        baseline_rate=baseline_rate_box.value/100
        mde_level=mde_level_box.value/100
        one_sided_test=one_sided_test_box.value
        power_level=statistic_power_box.value/100
        Bonfer_correction=Bonfer_correction_box.value
        if message==True:

            print(Fore.RED+ 'Checking input: ' + Style.RESET_ALL)

            print(f'  Test type                               : metric_type = {metric_type}')
            print()
            print(f'  Total groups including control group    : N = {N_groups}')
            print(f'  Confidence level                        : alpha = {alpha_level}')
            
            print(f'  Power needed                            : power = {power_level}')
            print(f'  Bonfer_correction                       : Bonfer_correction = {Bonfer_correction}')
            print(f'  Base line rate based on control offer   : Base line rate = {round(baseline_rate,4)}')
            print(f'  Minimum Detectable Effect               : mde = {mde_level}')
            print(f'  Testing one sided?                      : one_sided_test = {one_sided_test}')
            print()
     
        # N1, mde1, ci1,power1, p1,one_sided)
        out_put= calc_sample_size(N=N_groups,p=baseline_rate,ci=alpha_level,power=power_level,mde=mde_level,one_sided=one_sided_test,Bonf_correction=Bonfer_correction)
        print(Fore.RED+ 'Checking Output: ' + Style.RESET_ALL)
        print(f'  Calulating minimum sample size needed ... {out_put[0]:,}')
        print(f'  Base lift ... {round(out_put[1],4)}')
        print(f'  CohenD ... {round(out_put[2],4)}')
        if plot==True and  out_put[0]==  out_put[0]:
            print('Plotting')
            Nmin_list=[]
            lift_list=[.025,.05,.1,.15,.2,.25,.3]
            lift_list2_pct=[str(l*100) +'%' for l in lift_list]
            
            for l in lift_list:
                mde_level_new=baseline_rate*l
                out_put_new= exa1.calc_sample_size(N=N_groups,p=baseline_rate,ci=alpha_level,power=power_level,mde=mde_level_new,one_sided=one_sided_test,Bonf_correction=Bonfer_correction)
                Nmin_list.append(out_put_new[0])
            import matplotlib.pyplot as plt
            plt.figure(figsize=(12,12))
            plt.subplot(2,1,1)

            plt.plot(lift_list2_pct,Nmin_list,'o--', label='Sample size by Lift')
            
            for a,b in zip(lift_list2_pct, Nmin_list): 
               
                plt.text(a, b, str(f'{b:,}'), color='red')

            plt.xlabel('Lift')
            plt.ylabel('Sampe Size')
            plt.legend()
            plt.grid(True)
            plt.show()

            
                
    
    if metric_type=='Continuous metric':
        print('Calculating Nmin...')
    
        N_groups=Number_Of_Groups_box.value
        Bonfer_correction=Bonfer_correction_box.value
        conf_level=conf_level_box.value/100
        alpha_level=round(1-conf_level,2)
        Total_volume=Total_volume_box.value
        Sum_Square_volume=Sum_Square_volume_box.value
        mde_level=mde_level_vol_box.value
        Number_of_Visistor=Number_of_Visistor_box.value
        one_sided_test=one_sided_test_box.value
        power_level=statistic_power_box.value/100

        if message==True:
            print(Fore.RED+ 'Checking input: ' + Style.RESET_ALL)

            print(f'  Test type                               : metric_type = {metric_type}')
            print()
            print(f'  Total groups including control group    : N = {N_groups}')
            print(f'  Confidence level                        : alpha = {alpha_level}')
            print(f'  Bonfer_correction                       : Bonfer_correction = {Bonfer_correction}')
            print(f'  Power needed                            : power = {power_level}')
            print(f'  Minimum Detectable Effect               : mde = {mde_level}')
            print(f'  Testing one sided?                      : one_sided_test = {one_sided_test}')
            print()
        
        # N1, mde1, ci1,power1, p1,one_sided)
        out_put= calc_sample_size_vol_2(N=N_groups,sum_volume=Total_volume,sum_square_vol=Sum_Square_volume, number_of_visitor=Number_of_Visistor,ci=alpha_level,power=power_level,mde=mde_level,one_sided=one_sided_test,Bonf_correction=Bonfer_correction)
        print(Fore.RED+ 'Checking Output: ' + Style.RESET_ALL)
        print(f'  Calulating minimum sample size needed ... {out_put[0]:,}')
        print(f'  Base lift ... {round(out_put[1],4)}')
        print(f'  CohenD ... {round(out_put[2],4)}')
        if plot==True and out_put[0] ==  out_put[0]:
            Nmin_list=[]
            lift_list=[.025,.05,.1,.15,.2,.25,.3]
            lift_list2_pct=[str(l*100) +'%' for l in lift_list]
            
            
            for l in lift_list:
                mde_level_new=l*Total_volume/Number_of_Visistor
                out_put_new= exa1.calc_sample_size_vol_2(N=N_groups,sum_volume=Total_volume,sum_square_vol=Sum_Square_volume, number_of_visitor=Number_of_Visistor,ci=alpha_level,power=power_level,mde=mde_level_new,one_sided=one_sided_test,Bonf_correction=Bonfer_correction)
                Nmin_list.append(out_put_new[0])
            import matplotlib.pyplot as plt
            plt.figure(figsize=(12,12))
            plt.subplot(2,1,1)

            plt.plot(lift_list2_pct,Nmin_list,'o--', label='Sample size by Lift')
            
            for a,b in zip(lift_list2_pct, Nmin_list): 
                plt.text(a, b, str(f'{b:,}'), color='red')

            
            plt.xlabel('Lift')
            plt.ylabel('Sampe Size')
            plt.legend()
            plt.grid(True)
            plt.show()

# try
# N=calc_sample_size(N=2,p=.5,ci=.05,power=.8,mde=.25,one_sided=False,Bonf_correction=False)
# print(N)
# print('ok')