#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def request_api():
    url = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=ML&format=json'
    response = requests.get(url)
    return response

def df_micrlen(response):
    mlen = pd.DataFrame(response.json())
    return mlen

def renaming_cols(mlen):

    to_keep = ['pl_name', 'rastr', 'decstr', 'pl_masse', 'pl_massj', 'pl_orbsmax', 'sy_dist',
           'ml_dists', 'ml_xtimeein', 'ml_massratio', 'ml_magis', 'ml_radeinang']
    
    mlen = mlen[to_keep]
    
    new_names = ['planet_name',  'ra_event', 'dec_event', 'earth_massses', 'jupiter_masses', 
              'planet_orbmax', 'lens_distance', 'source_distance', 'einstein_cross_time', 'source_mag',
             'planet_star_mass_ratio', 'angular_einstein_radius']
    
    old_names = [name for name in mlen.columns]
    
    dict_names = (dict(zip(old_names, new_names)))
    
    mlen = mlen.rename(columns=dict_names)
    
    mlen = mlen.drop_duplicates('planet_name')
    
    return mlen

def wranglig(mlen):
   
    mlen['lens_distance_ly'] = mlen['lens_distance'] * 3.262
    
    mlen['source_distance_ly'] = mlen['source_distance'] * 3.262
    
    mlen['ra_event'] = mlen['ra_event'].str.replace(r'[hm]', ' ', regex=True).str.replace(r's', '', regex=True)
    
    mlen['ra_event'] = mlen['ra_event'].str.strip()
    
    mlen['dec_event'] = mlen['dec_event'].str.replace(r'[dm]', ' ', regex=True).str.replace(r's', '', regex=True)
    
    mlen.to_csv('microlensing_data.csv', index=False)
    
    return mlen


def request_api_second():
    url = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,sy_snum,sy_pnum,discoverymethod,disc_year,disc_telescope,pl_orbper,pl_orbsmax,pl_rade,pl_radj,pl_bmasse,pl_bmassj,pl_orbeccen,st_spectype,st_teff,st_rad,st_mass,sy_dist+from+pscomppars&format=json'
    response_2 = requests.get(url)
    return response_2
    
def df_pscomp(response):
    ps_comp = pd.DataFrame(response.json())
    return ps_comp

def renaming_cols_ps_comp(ps_comp):
    
    ps_comp = ps_comp.drop(columns='st_spectype')
    
    new_names_ps = ['planet_name', 'hostname', 'sys_num_stars', 'sys_num_planet', 'discovery_method', 
                'discovery_year', 'discovery_telescope', 'orbital_period', 'orbital_semi_major', 'planet_radius_earth',
               'planet_radius_jupiter', 'planet_mass_earth', 'planet_mass_jupiter', 'eccentricity', 'stellar_eff_temp',
               'stellar_radius', 'stellar_mass', 'dist_system']
    
    old_names_ps = [colum for colum in ps_comp.columns]
    
    dict_ps = dict(zip(old_names_ps, new_names_ps))
    
    ps_comp = ps_comp.rename(columns=dict_ps)
    
    return ps_comp

    
def wranglig_pscmop(ps_comp):
    
    ps_comp['dist_system_ly'] = ps_comp['dist_system'] * 3.262
    
    ps_comp.to_csv('ps_comp_data.csv', index=False)
    
    return ps_comp


def df_psmlen(ps_comp):
    
    ps_mlen = ps_comp.loc[ps_comp['discovery_method'] == 'Microlensing']
    
    return ps_mlen


def merge(ps_mlen, mlen):
    
    merged = pd.merge(mlen, ps_mlen, on='planet_name')
    
    merged = merged.drop(columns=['earth_massses', 'jupiter_masses', 'orbital_period', 'stellar_eff_temp', 'stellar_radius', 'eccentricity'], inplace=True)
    
    return merged


def analyze(ps_comp):
    
    hight_oper = ps_comp.sort_values('orbital_period', ascending=False).head(1)
    
    low_oper = ps_comp.sort_values('orbital_period').head(1)
    
    hight_oper.to_csv('hight_oper.csv', index=False)
    
    low_oper.to_csv('low_oper.csv', index=False)
    
    
def visualize_bar(ps_comp):
    
    bar = ps_comp['discovery_method'].value_counts().plot(kind='bar')
    
    bar_year = ps_comp['discovery_year'].value_counts().plot(kind='bar')
    
    fig_1 = bar.get_figure()
    
    fig_1.savefig('bar_discovery_method.png')
    
    fig_2 = bar_year.get_figure()
    
    fig_2.savefig('bar_year.png')
    

if __name__ == '__main__':
    request = request_api()
    df_1 = df_micrlen(request)
    df_re = renaming_cols(df_1)
    wrangle = wranglig(df_re)
    request_second = request_api_second()
    df_2 = df_pscomp(request_second)
    df_2_re = renaming_cols_ps_comp(df_2)
    wrangle_df2 = wranglig_pscmop(df_2_re)
    df_3 = df_psmlen(wrangle_df2)
    merge = merge(df_3, df_re)
    analysis = analyze(df_3)
    visual = visualize_bar(df_2_re)

