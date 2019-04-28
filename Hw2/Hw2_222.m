img_noise = imread('Image\lenna_noise.pgm');
img_original = imread('Image\lenna.pgm');

[x,y] = size(img_noise);
centerx = (x-1)/2;
centery = (y-1)/2;
[u,v] = meshgrid(-centerx:centerx,-centery:centery);
fshift = fftshift(fft2(img_noise));
D = sqrt(u.^2 + v.^2);

D20 = 20;
D50 = 50;
D100 = 100;

ideal20 = ifft2(ifftshift(double(D <= D20).*fshift));
ideal50 = ifft2(ifftshift(double(D <= D50).*fshift));
ideal100 = ifft2(ifftshift(double(D <= D100).*fshift));

origin = im2double(img_original);
ideal20_error = origin - ideal20;
ideal50_error = origin - ideal50;
ideal100_error = origin - ideal100;

ideal_RMS20 = sqrt(sum(sum(ideal20_error.^2))/(x*y));
ideal_RMS50 = sqrt(sum(sum(ideal50_error.^2))/(x*y));
ideal_RMS100 = sqrt(sum(sum(ideal100_error.^2))/(x*y));

figure('Name','Ideal low pass filter');
subplot(2,3,1);
imshow(img_original);
subplot(2,3,2);
imshow(img_noise);
subplot(2,3,3);
imshow(real(ideal20),[]);
subplot(2,3,4);
imshow(real(ideal50),[]);
subplot(2,3,5);
imshow(real(ideal100),[]);

%===============================================================================%
guass20 = ifft2(ifftshift(double(exp(-(D.^2./(2.*D20.^2)))).*fshift));
guass50 = ifft2(ifftshift(double(exp(-(D.^2./(2.*D50.^2)))).*fshift));
guass100 = ifft2(ifftshift(double(exp(-(D.^2./(2.*D100.^2)))).*fshift));

guass20_error = origin - guass20;
guass50_error = origin - guass50;
guass100_error = origin - guass100;

guass_RMS20 = sqrt(sum(sum(guass20_error.^2))/(x*y));
guass_RMS50 = sqrt(sum(sum(guass50_error.^2))/(x*y));
guass_RMS100 = sqrt(sum(sum(guass100_error.^2))/(x*y));

figure('Name','Guassian low pass filter');
subplot(2,3,1);
imshow(img_original);
subplot(2,3,2);
imshow(img_noise);
subplot(2,3,3);
imshow(real(guass20),[]);
subplot(2,3,4);
imshow(real(guass50),[]);
subplot(2,3,5);
imshow(real(guass100),[]);

%===============================================================================%
n = 5;
btw20 = ifft2(ifftshift(double(1./(1+(D./D20).^2*n)).*fshift));
btw50 = ifft2(ifftshift(double(1./(1+(D./D50).^2*n)).*fshift));
btw100 = ifft2(ifftshift(double(1./(1+(D./D100).^2*n)).*fshift));

btw20_error = origin - btw20;
btw50_error = origin - btw50;
btw100_error = origin - btw100;

btw_RMS20 = sqrt(sum(sum(btw20_error.^2))/(x*y));
btw_BRMS50 = sqrt(sum(sum(btw50_error.^2))/(x*y));
btw_BRMS100 = sqrt(sum(sum(btw100_error.^2))/(x*y));

figure('Name','Butterword low pass filter');
subplot(2,3,1);
imshow(img_original);
subplot(2,3,2);
imshow(img_noise);
subplot(2,3,3);
imshow(real(btw20),[]);
subplot(2,3,4);
imshow(real(btw50),[]);
subplot(2,3,5);
imshow(real(btw100),[]);

%median
img_pad = padarray(img_noise,[1 1],'both');
[x,y] = size(img_noise);
img_result = zeros(x,y);
for i = 1:x
    for k = 1:y
        result = zeros(9,1);
        count = 1;
        for m = 1:3
            for n = 1:3
                result(count) = img_pad(m+i-1,n+k-1);
                count = count + 1;
            end
        end
        result = sort(result);
        img_result(i,k) = result(5);
    end
end

img_result = uint8(img_result);
figure('Name', 'Median filter');
imshow(img_result);
med = double(img_result);
med_error = origin - med;
median_RMS = sqrt(sum(sum(med_error.^2))/(x*y));