file_list = dir('generated/generated');
occ_matrix = zeros([1000, 2000]); %[observations, variables]
for i = 3:length(file_list)
    file_dest = sprintf('generated/generated/%s',file_list(i).name);
    load(file_dest);
    occ = volumes;
    occ_vec = reshape(occ, [1,prod(size(occ))]);
    occ_matrix(i-2,:) = occ_vec;
end
occ_matrix_og = occ_matrix;
autoenc = trainAutoencoder(occ_matrix, 100);
out = predict(autoenc, occ_matrix);

thresh = 0.2;
occ = out;
s_ar_2 = size(occ);
for i = 1:s_ar_2(1)
    occ = reshape(occ(i,:),[10,10,20]);
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