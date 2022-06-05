import grpc
import rpc_files.scenario_pb2 as pb
import rpc_files.scenario_pb2_grpc as grp



with grpc.insecure_channel('localhost:50051') as channel:

    stub = grp.SimulationStub(channel)

    request = pb.ID(scenario_id=1)

    for feature in stub.RunSimulation(request):
        print(feature)