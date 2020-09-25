import glob
import subprocess as sp


print("\section{DMC extrapolation}")
print("Summaries of the zero time step linear extrapolation are plotted below. The blue shaded region corresponds to the error in the fit of the DMC energies at the three timesteps (0.001, 0.003, 0.005).")
count = 0
for i in sorted(glob.glob("../../extrapolation_plot/*png")):
    if count >= 3:
        # print("\\noindent\\makebox[\\textwidth]{\\rule{\\paperwidth}{0.4pt}}")
        print("%" * 79)
        # print("\\newpage")
        count = 0
    sp.call("cp {} ../images".format(i).split())

    filename = i.split("/")[-1]
    print(
        "\\includegraphics[width=\\textwidth,keepaspectratio]{{images/{}}}".format(
            filename
        )
    )
    count += 1
