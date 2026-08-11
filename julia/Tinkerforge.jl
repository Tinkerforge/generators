module Tinkerforge

using Sockets
using PyCall
using DataStructures
using DocStringExtensions

function __init__()
  include("src/ip_connection_base.jl")
end

include("ip_connection.jl")
include("devices/device_display_names.jl")
include("devices/device_factory.jl")

end
