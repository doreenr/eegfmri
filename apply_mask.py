
command_r = 'fslmaths /gablab/p/eegfmri/analysis/iaps/pilot009/segstats/aparc+aseg-in-func.nii -uthr 55 -thr 53 /gablab/p/eegfmri/analysis/iaps/pilot009/segstats/right_amygdala_mask.nii' 
a = os.system(command_r)
command_l = 'fslmaths /gablab/p/eegfmri/analysis/iaps/pilot009/segstats/aparc+aseg-in-func.nii -uthr 19 -thr 17 /gablab/p/eegfmri/analysis/iaps/pilot009/segstats/left_amygdala_mask.nii' 
a = os.system(command_l)

# try mri_binarize

def apply_mask(subject_id, bold):
    import nibabel as nb
    import pylab as pl
    from nilearn.masking import _load_mask_img, compute_epi_mask, apply_mask, _unmask_nd, _apply_mask_fmri
    from nilearn import _utils, resampling
    from nilearn._utils.ndimage import largest_connected_component
    from nilearn._utils.cache_mixin import cache
    ra = '/gablab/p/eegfmri/analysis/iaps/pilot%s/segstats/right_amygdala_mask.nii.gz' %(subject_id)
    ra = nb.load(ra)
    la = '/gablab/p/eegfmri/analysis/iaps/pilot%s/segstats/left_amygdala_mask.nii.gz' %(subject_id)
    la = nb.load(la)
    # f = _apply_mask_fmri(bold_1, b) and NiftiMasker do not work -- doing this manually:
    rd = _utils.as_ndarray(ra.get_data(),dtype=np.bool)
    ld = _utils.as_ndarray(la.get_data(),dtype=np.bool)
    rl = rd+ld
    mask_img = ra # or la 
    mask_data = rl
    mask_affine = mask_img.get_affine() # gets only affine of ra
    print 'Mask [ra] affine'
    print mask_affine
    print 'fMRI affine'
    print affine
    data = bold.get_data()
    series = _utils.as_ndarray(data, dtype=dtype, order="C", copy=True)
    X = series[mask_data].T
    # mask_img = mask_data.get_data()
    print 'Masked Data', X.shape
    u = _unmask_nd(X, mask_data)
    mean_img_u = np.mean(u, axis=3, dtype=float)
    figure(figsize=(20,5), dpi=80)
    pl.figure
    pl.title('Mask Amygdala')
    plt.imshow(np.rot90(mean_img_u[:, :, 5]), interpolation='nearest')
    return X

apply_mask('011', bold)
