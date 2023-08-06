from pathlib import Path
import logging
import click


logging.basicConfig(
    level=logging.DEBUG,
    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
    )

logger = logging.getLogger(__name__)

@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where to find CSV files to be converted to JSON.",
    type=str,
    )
@click.option(
    "--output",
    "-o",
    default="./",
    help="Path where the converted files will be saved.",
    type=str,
    )
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Separator used to split files.",
    type=str,
    )

def read_csv(input_path,delimiter:str=","):
    #Le o arquivo csv
    with input_path.open(mode='r') as file:
        data= file.readlines()


    parsed_data=[line.strip().split(delimiter) for line in data]
    return parsed_data

def parse_csv_to_json(data):
  #converte o CSV em Json
  column=data[0]
  lines=data[1:]
  result=[dict(zip(column,line))for line in lines]
  return result

def write_line(line,io,append_comma):
  key, value = line
  if append_comma:
    io.write(f't\t"{key}": "{value}",\n')
  else:
    io.write(f't\t"{key}": "{value}"\n')

def write_dictionary(data,io,append_comma):
  io.write("\t{\n")
  items=tuple(data.items())
  for line in items[:-1]:
    write_line(line,io,True)
  write_line(items[-1],io,False)
  io.write("\t}")
  if append_comma:
    io.write(",\n")
  else:
    io.write("\n")
    
def write_json_data(data,output_path):
    #Grava o json em um diretório
    with output_path.open(mode="w") as file:
      file.write("[\n")
      for d in data[:-1]:
        write_dictionary(d, file, append_comma=True)
      write_dictionary(data[-1],file, append_comma=False)
      file.write("]\n")

def json_reader(input):
    """Faz leitura de um ou mais arquivos .json"""
    with input.open(mode='r') as json_file:
        metadata = json_file.readlines()
    
    data = [line.strip().replace("[", "").replace("]","").replace("{", "").replace("}","").replace('"', "").replace("\n", "") for line in metadata]
    data = list(filter(None, data))
    return data

def json2csv(data):
    """Converte list (Lista) para dict (Dicionario, mapa, json)"""
    headers = list()
    lines = list()
    for i in data:
        line_data = i.split(",")
        line_data = list(filter(None, line_data))
        for l in line_data:
            header = l.strip().split(":")[0]
            line = l.strip().split(":")[1]
            headers.append(header)
            lines.append(line)
    headers = list(dict.fromkeys(headers))
    return headers, lines


def iter_csv(headers: list, lines: list, file, delimiter: str = ","):
    """Organiza arquivo dict em um formato csv valido"""
    
    line_break = len(headers)
    for h in headers[:-1]:
        file.write(h+delimiter)
    file.write(headers[-1]+"\n")
    count = 0
    for line in lines:
        count += 1
        if count == line_break:
            file.write(line+"\n")
            count = 0
        else:
            file.write(line+delimiter)
        
def save_csv(headers: list, lines: list, output: Path, delimiter: str = ","):
    """Salva o arquivo .csv em disco"""
    with output.open(mode='w') as csv_file:
        
        iter_csv(headers, lines, csv_file, delimiter)

def json_converter(input, output, delimiter: str = ","):
    """Converte arquivos .json para arquivos .csv"""
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input path: %s", input_path)
    logger.info("Output path: %s", output_path)

    for i in input_path.iterdir():
        if str(i).split(".")[-1] == "json":
            logger.info("Current file: %s", i)
            data = json_reader(i)
            headers, lines = json2csv(data)
            save_csv(headers, lines, output_path, delimiter)