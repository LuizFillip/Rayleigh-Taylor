from RayleighTaylor import plot_winds_effect 
from utils import save_but_not_show
import os


def save_plot(infile, filename, to_folder):
    
    effect = to_folder.split("_")[0]
    
    for hemisphere in ["south", "north"]:
        
        fig = plot_winds_effect(
            os.path.join(infile, filename), 
            hemisphere, effect = effect)
        
        FigureName = filename.replace(".txt", ".png")
        save_in = f"D:\\plots\\{to_folder}\\{hemisphere}_{FigureName}"
        
        save_but_not_show(fig, save_in)
        
  
def main():
    infile = "database/RayleighTaylor/process/"
    
    for to_folder in ["winds_effect",
                      "recombination_winds_effect"]:
    
        for filename in os.listdir(infile):
            print("saving...", filename)
            save_plot(infile, filename, to_folder)