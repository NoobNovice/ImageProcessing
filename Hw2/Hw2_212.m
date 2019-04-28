img = imread('Image\Cross.pgm');
[x,y] = size(img);
center_x = (x-1)/2;
center_y = (y-1)/2;
[u,v] = meshgrid(-center_x:center_x,-center_y:center_y);
D = sqrt(u.^2 + v.^2);

fshift = fftshift(fft2(img));

D20 = 20;
D50 = 50;
D100 = 100;

ideal20 = ifft2(ifftshift(double(D <= D20).*fshift));
ideal50 = ifft2(ifftshift(double(D <= D50).*fshift));
ideal100 = ifft2(ifftshift(double(D <= D100).*fshift));

figure('Name','Ideal low pass filter');
subplot(2,2,1);
imshow(img);
subplot(2,2,2);
imshow(real(ideal20),[]);
subplot(2,2,3);
imshow(real(ideal50),[]);
subplot(2,2,4);
imshow(real(ideal100),[]);

figure('Name','Ideal filter 20');
Z = double(D<=D20);
surf(u,v,Z);

%===============================================================================%
guass20 = ifft2(ifftshift(double(exp(-(D.^2./(2.*D20.^2)))).*fshift));
guass50 = ifft2(ifftshift(double(exp(-(D.^2./(2.*D50.^2)))).*fshift));
guass100 = ifft2(ifftshift(double(exp(-(D.^2./(2.*D100.^2)))).*fshift));

figure('Name','Guassian low pass filter');
subplot(2,2,1);
imshow(img);
subplot(2,2,2);
imshow(real(guass20),[]);
subplot(2,2,3);
imshow(real(guass50),[]);
subplot(2,2,4);
imshow(real(guass100),[]);

figure('Name','Guassian filter 20');
Z = double(exp(-(D.^2./(2.*D20.^2))));
surf(u,v,Z);

%===============================================================================%
n = 2;
btw20 = ifft2(ifftshift(double(1./(1+(D./D20).^2*n)).*oriShift));
btw50 = ifft2(ifftshift(double(1./(1+(D./D50).^2*n)).*oriShift));
btw100 = ifft2(ifftshift(double(1./(1+(D./D100).^2*n)).*oriShift));

figure('Name','Butterword low pass filter');
subplot(2,2,1);
imshow(img);
subplot(2,2,2);
imshow(real(btw20),[]);
subplot(2,2,3);
imshow(real(btw50),[]);
subplot(2,2,4);
imshow(real(btw100),[]);

figure('Name','Butterword filter 20');
Z = double(1./(1+(D./D100).^2*n));
surf(u,v,Z);