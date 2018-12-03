%load('mats/mats/output1017.scad.mat');
load('generated/generated/gen_0000.mat');

thresh = 0.2;
occ = volumes;
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