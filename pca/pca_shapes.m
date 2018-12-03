load('pca_ws_binary.mat')
thresh = .5;
rng('default');
approximationRank15 = score(:,1:15) * coeff(:,1:15)' + repmat(mu, size_occ_m(1), 1);
s_ar = size(approximationRank15);
for i = randperm(size(s_ar, 1))
    clf;
    title('PCA');
    occ_og = reshape(occ_matrix_og(i,:),[10,10,20]);
    occ_og(occ_og <= thresh) = 0;
    occ_og(occ_og > thresh) = 1;
    occ_og = logical(occ_og);
    [x, y, z] = meshgrid(1:size(occ_og, 1), 1:size(occ_og, 2), 1:size(occ_og, 3));
    x = x(:);
    y = y(:);
    z = z(:);
    ptcloud = pointCloud([x(occ_og), y(occ_og), z(occ_og)]);    
    subplot(1,2,1);
    hold on;
    pcshow(ptcloud, 'MarkerSize', 1000);
    pcshow([x(~occ_og), y(~occ_og), z(~occ_og)], [1, 0, 0]);
    hold off;
    orig_title = sprintf('original %d', i);
    title(orig_title);
    
    %ax1_copy = copyobj(ax1,fnew);
    %subplot(1,2,1,ax1_copy)
    
    occ = reshape(approximationRank15(i,:),[10,10,20]);
    occ(occ <= thresh) = 0;
    occ(occ > thresh) = 1;
    occ = logical(occ);

    ptcloud = pointCloud([x(occ), y(occ), z(occ)]);
    subplot(1,2,2);
    hold on;
    pcshow(ptcloud, 'MarkerSize', 1000);
    pcshow([x(~occ), y(~occ), z(~occ)], [1, 0, 0]);
    hold off;
    recon_title = sprintf('reconstructed %d', i);
    title(recon_title);
    %ax2_copy = copyobj(ax2,fnew);
    %subplot(1,2,2,ax2_copy)
    
    waitforbuttonpress;

end