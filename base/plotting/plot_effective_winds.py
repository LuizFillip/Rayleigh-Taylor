

U = effective_wind()
d, i = run_igrf(date, 
                site = site, 
                alt = alt)
d, i = round(d, 3), round(i, 3)
print(site, i, d)