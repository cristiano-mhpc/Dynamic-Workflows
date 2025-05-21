params.str = "Hello world!"

include { splitString as splitString } from './processes/split.nf'
include { convertToUpper as convertToUpper } from './processes/upper.nf'

workflow {
    ch_str = channel.of(params.str)
    ch_chunks = splitString(ch_str)
    convertToUpper(ch_chunks.flatten())
}