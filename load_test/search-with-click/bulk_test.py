import subprocess
from bs4 import BeautifulSoup

from tqdm import tqdm

def test(name:str):
    jmx_name=f'{name}.jmx'

    for n_users in tqdm(range(50, 550, 50)):
        
        with open(jmx_name) as f:
            Bs_data = BeautifulSoup(f.read(), "xml")
            tag=Bs_data.find('intProp', {"name":"ThreadGroup.num_threads"})
            tag.string = str(n_users)
        
        with open(jmx_name, 'w') as f:
            f.write(str(Bs_data))
        
        results_path = f'results_{n_users}'
        
        subprocess.Popen(f'jmeter -n -t {jmx_name} -l {results_path+"/results.csv"} -e -o {results_path}', shell=True, stdout=subprocess.DEVNULL).wait()
        
if __name__ == "__main__":
    test('search-with-click')