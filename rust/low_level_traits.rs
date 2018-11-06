pub trait LowLevelRead<DataT, ResultT> {
    fn ll_message_length(&self) -> usize;
    fn ll_message_chunk_offset(&self) -> usize;
    fn ll_message_chunk_data(&self) -> &[DataT];
    fn get_result(&self) -> ResultT;
}

pub trait LowLevelWrite<ResultT> {
    fn ll_message_written(&self) -> usize;
    fn get_result(&self) -> ResultT;
}
