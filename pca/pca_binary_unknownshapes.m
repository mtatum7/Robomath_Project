load('pca_ws_binary.mat')
file_list = dir('generated_test/generated_test');
new_shape_occm = zeros([200, 2000]); %[observations, variables]
for i = 3:length(file_list)
    file_dest = sprintf('generated_test/generated_test/%s',file_list(i).name);
    load(file_dest);
    thresh = 0.2;
    new_shape_occ = volumes;
    new_shape_occ(new_shape_occ < thresh) = 0;
    new_shape_occ(new_shape_occ >= thresh) = 1;
    new_shape_occ = logical(new_shape_occ);
    occ_vec = reshape(new_shape_occ, [1,prod(size(new_shape_occ))]);
    new_shape_occm(i-2,:) = occ_vec;
end
new_shape_occm_og = new_shape_occm;
%[coeff, score, latent, tsquared, explained, mu] = pca(occ_matrix);
new_score = coeff(:,1:15)'/new_shape_occm;
approximationRank15 = new_score' * coeff(:,1:15)' + repmat(mu, size(new_shape_occm,1), 1);
approx = approximationRank15;
thresh = 0.2;
s_ar_2 = size(approx);
for i = 1:s_ar_2(1)
    occ = reshape(approx(i,:),[10,10,20]);
    occ(occ < thresh) = 0;
    occ(occ >= thresh) = 1;
    occ = logical(occ);
    [x, y, z] = meshgrid(1:size(occ, 1), 1:size(occ, 2), 1:size(occ, 3));

    x = x(:);
    y = y(:);
    z = z(:);

    ptcloud = pointCloud([x(occ), y(occ), z(occ)]);
    
    hold on;
    pcshow(ptcloud, 'MarkerSize', 1000);
    pcshow([x(~occ), y(~occ), z(~occ)], [1, 0, 0]);
end