import os
import subprocess
import sys

def generate_proto():
    """
    Generate Python code from proto files
    """
    proto_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'protos')
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generated')
    
    os.makedirs(output_dir, exist_ok=True)
    
    init_file = os.path.join(output_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Generated code')
    
    proto_files = [f for f in os.listdir(proto_dir) if f.endswith('.proto')]
    
    if not proto_files:
        print(f"No proto files found in {proto_dir}")
        return False
    
    for proto_file in proto_files:
        proto_path = os.path.join(proto_dir, proto_file)
        
        cmd = [
            sys.executable, '-m', 'grpc_tools.protoc',
            f'--proto_path={proto_dir}',
            f'--python_out={output_dir}',
            f'--grpc_python_out={output_dir}',
            proto_path
        ]

        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Successfully generated code from {proto_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating code from {proto_file}: {e.stderr}")
            return False
    
    return True

if __name__ == "__main__":
    print("Generating Python code from proto files...")
    success = generate_proto()
    sys.exit(0 if success else 1) 