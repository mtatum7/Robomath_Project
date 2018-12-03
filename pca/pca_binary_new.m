file_list = dir('generated/generated');
occ_matrix = zeros([1000, 2000]); %[observations, variables]
for i = 3:length(file_list)
    file_dest = sprintf('generated/generated/%s',file_list(i).name);
    load(file_dest);
    thresh = 0.2;
    occ = volumes;
    occ(occ < thresh) = 0;
    occ(occ >= thresh) = 1;
    occ = logical(occ);
    %occ = occ(:,:,1:15);
    occ_vec = reshape(occ, [1,prod(size(occ))]);
    occ_matrix(i-2,:) = occ_vec;
end
[coeff, score, latent, tsquared, explained, mu] = pca(occ_matrix);
size_occ_m = size(occ_matrix);
reconstructed = score * coeff' + repmat(mu, size_occ_m(1),1);
ex = explained;
approximationRank2 = score(:,1:2) * coeff(:,1:2)' + repmat(mu, size_occ_m(1), 1);
approximationRank5 = score(:,1:5) * coeff(:,1:5)' + repmat(mu, size_occ_m(1), 1);
perfectApprox = score * coeff' + repmat(mu, size_occ_m(1), 1);
approx = perfectApprox;
sum(sum((occ_matrix - perfectApprox).^2));
size(coeff(:,1:2)');
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