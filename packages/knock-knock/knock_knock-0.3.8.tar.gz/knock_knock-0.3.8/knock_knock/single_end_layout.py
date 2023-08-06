from hits import sam

import knock_knock.layout

class SingleEndLayout(knock_knock.layout.Categorizer):
    ''' Base class for categorizers of single-end reads
    that are expected to start at a primer but not necessarily
    reach the other primer.
    '''

    def __init__(self, alignments, target_info, error_corrected=False, mode=None):
        self.alignments = [al for al in alignments if not al.is_unmapped]
        self.target_info = target_info
        
        alignment = alignments[0]
        self.query_name = alignment.query_name
        self.seq = sam.get_original_seq(alignment)
        if self.seq is None:
            self.seq = ''

        self.seq_bytes = self.seq.encode()
        self.qual = np.array(sam.get_original_qual(alignment))

        self.primary_ref_names = set(self.target_info.reference_sequences)

        self.required_sw = False

        self.special_alignment = None
        
        self.relevant_alignments = self.alignments

        self.ins_size_to_split_at = 3
        self.del_size_to_split_at = 2

        self.error_corrected = error_corrected
        self.mode = mode

        self.trust_inferred_length = True
