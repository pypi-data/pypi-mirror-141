rom="""if not terminating:
    rom_simulation = simulation.ROM()
    params = simulation.ROMParameters()
    model_params = params.ModelParameters()

    model_params.name = '{}'+'_'+'{}'
    model_params.inlet_face_names = [str(inlet)]
    model_params.outlet_face_names = [str(o) for o in outlets]
    model_params.centerlines_file_name = '{}' + os.sep +'centerlines.vtp'

    mesh_params = params.MeshParameters()

    fluid_params = params.FluidProperties()
    material = params.WallProperties.OlufsenMaterial()

    bcs = params.BoundaryConditions()
    bcs.add_velocities(face_name=str(inlet),file_name='{}'+os.sep+'{}')
    for face_name in outlets:
        bcs.add_resistance(face_name=str(face_name),resistance=1/resistance[face_name])
    solution_params = params.Solution()
    solution_params.time_step = {}
    solution_params.num_time_steps = {}
    outdir = '{}'
    rom_simulation.write_input_file(model_order={},model=model_params,
                                    mesh=mesh_params,fluid=fluid_params,
                                    material=material,boundary_conditions=bcs,
                                    solution=solution_params,directory=outdir)
    if {} == 0:
        run_rom = open('{}'+os.sep+'run.py','w+')
        run_rom_file = ''
        path = sv.__path__[0].replace(os.sep+'sv','')
        run_rom_file += 'import os\\n'
        run_rom_file += 'import sys\\n'
        run_rom_file += "sys.path.append('{{}}')\\n".format(path)
        run_rom_file += 'from svZeroDSolver import svzerodsolver\\n'
        input_file = '{}'+os.sep+'solver_0d.in'
        if 'Windows' in platform.system():
            input_file = input_file.replace(os.sep,os.sep+os.sep)
        run_rom_file += "svzerodsolver.solver.set_up_and_run_0d_simulation('{{}}')\\n".format(input_file)
        run_rom.writelines([run_rom_file])
        run_rom.close()
"""
