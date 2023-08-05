# Function's library of the package

import os
import halcon as ha
import json

class HalconProgram:

    def __init__(self, ProgramName, ProgramPath):
        self.ProgramName = ProgramName
        self.ProgramPath = ProgramPath

    def loadProgram(self):
        Program = ha.HDevProgram(os.path.join(self.ProgramPath, self.ProgramName))
        return Program

    def executeProgram(self):
        Program = ha.HDevProgram(os.path.join(self.ProgramPath, self.ProgramName))
        exprogram = ha.HDevProgramCall(Program)
        exprogram.execute()
        return exprogram

    def getResults(self):

        # generate JSON sub-lists
        Control_Variables = {}
        Iconic_Variables = {}

        # load program
        Program = self.loadProgram()

        # execute program
        Executed = self.executeProgram()

        # add data to sub-lists
        for i, j in enumerate(Program.control_var_names):
            Control_Variables[j] = Executed.get_control_var_by_name(j)
        for i, j in enumerate(Program.inconic_var_names):
            Iconic_Variables[j] = Executed.get_iconic_var_by_name(j)

        # generate JSON result
        Results={}

        # add data to JSON result
        Results['Control Variables'] = Control_Variables
        Results['Iconic Variables'] = Iconic_Variables
        return Results

    def saveToJSON(self):
        Results=self.getResults()
        Results=Results['Control Variables']
        if 'OCRHandle' in Results.keys():
            del Results['OCRHandle']
        l=len(self.ProgramName)
        Name=self.ProgramName [:l-5]  
        # save JSON file into folder
        with open(Name+'.json', 'w', encoding='utf-8') as f:
            json_string = json.dump(Results, f, ensure_ascii=False, indent=4)
        print('JSON File '+'"'+self.ProgramName+'"'+'successfully written!')
        return





