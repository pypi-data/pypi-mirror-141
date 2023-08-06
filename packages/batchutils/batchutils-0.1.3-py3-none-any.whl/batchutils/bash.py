import hailtop.batch as hb


def concat_job(b, infiles, n_cpu=1):
    j = b.new_job(name='concat-files')
    j.image('gcr.io/daly-neale-sczmeta/hailgenetics-python-dill-pandas:0.1.0')
    j.cpu(n_cpu)
    j.memory('highmem')
    j.storage('20Gi')
    cmd = f'''cat {" ".join(infiles)} > {j.ofile}'''
    j.command(cmd)
    return j


def concat_and_append_header_job(b, infiles, header_list, n_cpu=1):
    j = b.new_job(name='concat_and_append_header_job')
    j.image('gcr.io/daly-neale-sczmeta/hailgenetics-python-dill-pandas:0.1.0')
    j.cpu(n_cpu)
    j.memory('highmem')
    j.storage('20Gi')
    header_str = "\t".join(header_list)
    cmd = f'''echo -e "{header_str}" | cat - {' '.join(infiles)} > {j.ofile}'''
    j.command(cmd)
    return j


def gzip_chain_job(j):
    cmd = f'gzip -c -f {j.ofile} > tmp.gzip.chain.gz; mv tmp.gzip.chain.gz {j.ofile}'
    j.command(cmd)
    return j
