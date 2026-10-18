"""Challenge II.2: one copy of the course script convergence_test_si.py per pseudopotential.
Only the pseudopotential file, pseudo_dir, the pw.x command and (for ultrasoft PPs) ecutrho are
changed; convergence logic, test ranges and tolerance (0.01 meV/atom) stay identical."""
import os, re
SYS_PP = '/usr/share/espresso/pseudo'
PPS = {'dojo-NC-PBE':   (os.path.abspath('.'), 'Si.upf', None),
       'rrkjus-US-PBE': (SYS_PP, 'Si.pbe-nl-rrkjus_psl.1.0.0.UPF', 8),
       'vbc-NC-LDA':    (SYS_PP, 'Si.pz-vbc.UPF', None)}
src = open('convergence_test_si.py').read()
for label, (pdir, pfile, ratio) in PPS.items():
    s = src.replace("pseudopotentials = {'Si': 'Si.upf'}", f"pseudopotentials = {{'Si': '{pfile}'}}")
    s = s.replace("pseudo_dir='./'", f"pseudo_dir='{pdir}'")
    s = re.sub(r"^pw_command = .*$", "pw_command = 'mpirun -np 6 pw.x'", s, flags=re.M)
    if ratio:
        s = re.sub(r"^(\s*)(input_data\['system'\]\['ecutwfc'\] = .*)$",
                   rf"\1\2\n\1input_data['system']['ecutrho'] = {ratio} * input_data['system']['ecutwfc']", s, flags=re.M)
    os.makedirs(f'pp_{label}', exist_ok=True)
    open(f'pp_{label}/convergence_test_si_{label}.py', 'w').write(s)
    print(f'written pp_{label}/convergence_test_si_{label}.py')
