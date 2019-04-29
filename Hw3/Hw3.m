img = imread('Image\WormHole_1H.tif');
img = rgb2gray(img);
img = double(img);
% Laplacian
kernel = [0,1,0;1,-4,1;0,1,0];
[l,o] = size(kernel);
img_pad = padarray(img,[1 1],'both');
[x,y] = size(img);
lf = zeros(x,y);
for i = 1:x
    for j = 1:y
        result = 0;
        for m = 1:l
            for n = 1:o
                con = double(kernel(m,n)).*double(img_pad(m+i-1,n+j-1));
                result = result + con; 
            end
        end
        lf(i,j) = double(result);
    end
end
img_edge = double(img - lf);
figure('Name','img_edge1')
imshow(img_edge)
figure('Name','WormHole_1H')
imshowpair(img_edge,img,'montage')
axis off
sobel = edge(img_edge,'Sobel');
[centers, radii] = imfindcircles(sobel,[5 13]);
viscircles(centers, radii,'Color','b');

%=========================================================================%
img = imread('Image\WormHole_2H.tif');
img = rgb2gray(img);
img = double(img);
% Laplacian
kernel = [0,1,0;1,-4,1;0,1,0];
[l,o] = size(kernel);
img_pad = padarray(img,[1 1],'both');
[x,y] = size(img);
lf = zeros(x,y);
for i = 1:x
    for j = 1:y
        result = 0;
        for m = 1:l
            for n = 1:o
                con = double(kernel(m,n)).*double(img_pad(m+i-1,n+j-1));
                result = result + con; 
            end
        end
        lf(i,j) = double(result);
    end
end
img_edge = double(img - lf);
figure('Name','img_edge2')
imshow(img_edge)
figure('Name','WormHole_2H')
imshowpair(img_edge,img,'montage')
axis off
sobel = edge(img_edge,'Sobel');
[centers, radii] = imfindcircles(sobel,[5 13]);
viscircles(centers, radii,'Color','b');