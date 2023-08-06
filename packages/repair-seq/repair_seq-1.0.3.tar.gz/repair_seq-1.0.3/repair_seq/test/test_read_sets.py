import textwrap
from pathlib import Path

import yaml

import hits.utilities
import hits.sam
import knock_knock.target_info

memoized_property = hits.utilities.memoized_property

base_dir = Path(__file__).parent

class ReadSet:
    def __init__(self, set_name):
        self.set_name = set_name

        self.dir = base_dir / 'read_sets' / self.set_name
        
        self.bam_fn =  self.dir / 'alignments.bam'
        self.expected_values_fn = self.dir / 'expected_values.yaml'

    @memoized_property
    def details(self):
        return yaml.safe_load(self.expected_values_fn.read_text())

    @memoized_property
    def expected_values(self):
        return self.details['expected_values']

    def get_read_layout(self, read_id):
        layout = None

        for qname, als in hits.sam.grouped_by_name(self.bam_fn):
            if qname == read_id:
                layout = self.categorizer(als, self.target_info)
                break

        if layout is None:
            raise ValueError(read_id)
        
        return layout

    @memoized_property
    def target_info(self):
        target_info_name = self.details['target_info']
        supplemental_index_names = ['hg19', 'bosTau7', 'e_coli']
        supplemental_indices = knock_knock.target_info.locate_supplemental_indices(base_dir)
        supplemental_indices = {name: supplemental_indices[name] for name in supplemental_index_names}
        target_info = knock_knock.target_info.TargetInfo(base_dir,
                                                         target_info_name,
                                                         supplemental_indices=supplemental_indices,
                                                         **self.details.get('target_info_kwargs', {}),
                                                        )

        return target_info

    @memoized_property
    def categorizer(self):
        if self.details['experiment_type'] == 'twin_prime':
            from repair_seq.twin_prime_layout import Layout
            categorizer = Layout
        elif self.details['experiment_type'] == 'prime_editing_layout':
            from repair_seq.prime_editing_layout import Layout
            categorizer = Layout
        else:
            raise NotImplementedError

        return categorizer
    
def test_read_sets():
    read_set_dirs = sorted([p for p in (base_dir / 'read_sets').iterdir() if p.is_dir()])

    # Ensure that at least one read set was found. 
    assert len(read_set_dirs) > 0

    discrepancies = []

    for read_set_dir in read_set_dirs:
        set_name = read_set_dir.name

        read_set = ReadSet(set_name)

        num_tested = 0

        for qname, als in hits.sam.grouped_by_name(read_set.bam_fn):
            try:
                layout = read_set.categorizer(als, read_set.target_info)
                layout.categorize()

                category = layout.category
                subcategory = layout.subcategory

            except:
                category = 'error'
                subcategory = 'error'

            expected = read_set.expected_values[qname]

            if expected['category'] != category or expected['subcategory'] != subcategory:
                discrepancies.append((set_name, qname, expected, category, subcategory))

            num_tested += 1

        print(f'Tested {num_tested: >3d} sequences for {set_name}.') 

    diagnostic_messages = []
    for set_name, qname, expected, category, subcategory in discrepancies:

        diagnostic_message = f'''
            set name: {set_name}
            query name: {qname}
            expected: ({expected["category"]}, {expected["subcategory"]})
            actual: ({category}, {subcategory})
            note: {expected["note"]}
        '''

        diagnostic_messages.append(textwrap.dedent(diagnostic_message))
    
    full_diagnostic_message = '\n'.join(diagnostic_messages)
    assert len(discrepancies) == 0, full_diagnostic_message