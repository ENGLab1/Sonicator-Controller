from Sonicator_Setup import Arduino_Sonicator

def main():
    sonicator = Arduino_Sonicator()
    sonicator.sonicate()

if __name__ == "__main__": main()  