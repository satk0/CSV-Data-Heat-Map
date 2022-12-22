# generateCSV.py - generate random numbers to CSV file

import argparse
import random
import aiofiles
import asyncio

parser = argparse.ArgumentParser(description="Generate 2D array of random numbers to CSV file")
parser.add_argument('-m', type=str, dest='m',
        help="Number of rows to generate")
parser.add_argument('-n', type=str, dest='n',
        help="Number of columns to generate")
parser.add_argument('-filename',metavar='-f',type=str, dest='fname',
        help="Name of the file to save data")

async def main():
    args = parser.parse_args()

    print(args.m, args.n)

    rows = int(args.m)
    cols = int(args.n)


    async with aiofiles.open(args.fname, 'w+') as f:
        await f.write('cr;')
        for colNum in range(cols-1):
            await f.write('c{colNum};'.format(colNum=colNum))
        await f.write('c{colNum}'.format(colNum=cols-1))

        await f.write('\n')
        for rowNum in range(rows):
            await f.write('r{rowNum};'.format(rowNum=rowNum))
            for colNum in range(cols-1):
                await f.write('{};'.format(round(random.uniform(1, 30), 3))) 
            await f.write('{}'.format(round(random.uniform(1, 30), 3))) 
            await f.write('\n')
#    for colNum in range(cols):

asyncio.run(main())        
