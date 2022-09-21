import scanpy as sc


def test_scgen(adata, model, example_pert='KLF1'):
    ctrl_adata = adata[adata.obs.perturbation_name.isin(['control', example_pert])]
    sc.tl.rank_genes_groups(ctrl_adata, groupby='perturbation_name', reference='control', method='wilcoxon')

    diff_genes = ctrl_adata.uns['rank_genes_groups']['names'][example_pert]
    print('Differentially expressed genes found in example perturbation {}: \n {}'.format(
        example_pert, diff_genes[:10]))

    pred, delta = model.predict(
        ctrl_key='control',
        stim_key=example_pert,
        adata_to_predict=adata[adata.obs.perturbation_name == 'control'].copy()  # strange implementation but ok
    )
    pred.obs['perturbation_name'] = 'pred'

    eval_adata = pred.concatenate(ctrl_adata)[:, diff_genes[:100]]

    r2_value_ground_truth = model.reg_mean_plot(
        eval_adata,
        axis_keys={'x': 'pred', 'y': example_pert},
        gene_list=diff_genes[:20],
        labels={'x': 'predicted', 'y': 'ground truth'},
        show=True,
        legend=False
    )

    r2_value_no_treatment = model.reg_mean_plot(
        eval_adata,
        axis_keys={'x': 'pred', 'y': 'control'},
        gene_list=diff_genes[:20],
        labels={'x': 'predicted', 'y': 'no treatment'},
        show=True,
        legend=False
    )
    return r2_value_ground_truth, r2_value_no_treatment

