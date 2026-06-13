module PyTinkerforge

using Sockets
using PyCall
using Conda
using DocStringExtensions

function __init__()
  try
    tinkerforge = pyimport("tinkerforge")
  catch e
    Conda.pip_interop(true)
    Conda.pip("install", "Tinkerforge")
  end
end

include("ip_connection.jl")
include("devices/device_display_names.jl")
include("devices/device_factory.jl")

end
