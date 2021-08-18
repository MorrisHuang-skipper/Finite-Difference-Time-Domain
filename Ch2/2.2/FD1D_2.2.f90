!========================================================
!   Purpose: adding Fourier transform
!
!   Methods: Fourier Transform
!       
!       Date        Programer       Description of change
!       ====        =========       =====================
!      9/7/20        MorrisH        Original Code
!========================================================
PROGRAM main
    IMPLICIT NONE
    ! number of cells to be used
    INTEGER(8), PARAMETER :: Ncell = 200
    REAL(8), PARAMETER :: pi = 3.14159265359
    INTEGER(8) :: k, m, kc, T, kstart
    REAL(8) :: Dx(Ncell), Ex(Ncell), Hy(Ncell)
    REAL(8) :: ga(Ncell), gb(Ncell)
    REAL(8) :: ix(Ncell)
    REAL(8) :: t0, width, pulse, eps, epsz
    REAL(8) :: ddx, dt, freq_in, sigma
    REAL(8) :: Ex_low_m1, Ex_high_m1
    REAL(8) :: Ex_low_m2, Ex_high_m2
    REAL(8) :: real_pt(5, Ncell), imag_pt(5, Ncell)
    REAL(8) :: freq(5), arg(5), ampn(5, Ncell)
    REAL(8) :: phasen(5, Ncell), real_in(5)
    REAL(8) :: imag_in(5), amp_in(5), phase_in(5)
    REAL(8) :: mag(Ncell)
    ! name of write file
    CHARACTER(len=15) :: str1
    CHARACTER(len=8) :: fmt
    fmt = '(I3.3)'

    ! initialize to free space
    Ex = 0.0
    Hy = 0.0
    Dx = 0.0
    ga = 1.0
    gb = 0.0
    ix = 0.0
    mag = 0.0
    ! initialize Fourier transform para
    real_pt = 0.0
    imag_pt = 0.0
    ampn = 0.0
    phasen = 0.0
    real_in = 0.0
    imag_in = 0.0
    amp_in = 0.0
    phase_in = 0.0
    ! initialize bd condition
    Ex_low_m1 = 0
    Ex_high_m1 = 0
    Ex_low_m2 = 0
    Ex_high_m2 = 0
    ! center of the problem space
    kc = Ncell / 2
    ! center of the incident pulse
    t0 = 50.0
    ! width of the incident pulse
    width = 10.0
    ! epsilon value
    eps = 4
    epsz = 8.85419E-12
    ! start of dielectric medium
    Kstart = 100
    ! cell size to 1 m
    ddx = 0.01
    ! time step
    dt = ddx / (2 * 3E8)
    ! frequency of input pulse
    freq_in = 500E6
    ! conductivity
    sigma = 0.00
    ! para for the Fourier Transfrom
    freq = (/ 100.0E6, 200.0E6, 500.0E6, 0.0, 0.0 /)
    arg = 2 * pi * freq * dt

    dielectric: do k = Kstart, Ncell
        ga(k) = 1.0 / (eps + sigma * dt / epsz)
        gb(k) = sigma * dt / epsz
    end do dielectric
    

    steploop: do T = 0, 400
        !!! START FDTD !!!
        ! calculate Dx field
        Dfield: do k = 2, Ncell
            Dx(k) = Dx(k) + 0.5 * (Hy(k-1) - Hy(k))
        end do Dfield

        ! put gaussian pulse in the center
        pulse = exp(-0.5 * ((t0 - T) / width) ** 2.0)
        Dx(5) = Dx(5) + pulse

        ! calculate Ex-field form Dx
        Efield: do k = 1, Ncell-1
            Ex(k) = ga(k) * (Dx(k) - ix(k))
            ix(k) = ix(k) + gb(k) * Ex(k)
        end do Efield

        ! Calculate the Fourier tramsform of Ex
        do k = 1, Ncell
            do m = 1, 3
                real_pt(m, k) = real_pt(m, k) + &
                                cos(arg(m) * T) * Ex(k)
                imag_pt(m, k) = imag_pt(m, k) - &
                                sin(arg(m) * T) * Ex(k)
            end do
        end do
        ! Fourier transform of the input pulse
        if (T < 2 * t0) then
            do m = 1, 3
                real_in(m) = real_in(m) + cos(arg(m) * T) &
                             * Ex(10)
                imag_in(m) = imag_in(m) - sin(arg(m) * T) &
                             * Ex(10)
            end do
        end if

        ! Absorbing Boundary Condition
        ! Ex(0)_n = Ex(1)_n-2
        Ex(1) = Ex_low_m2
        Ex_low_m2 = Ex_low_m1
        Ex_low_m1 = Ex(2)
        ! Ex(Ncell)_n = Ex(Ncell-1)_n-2
        Ex(Ncell) = Ex_high_m2
        Ex_high_m2 = Ex_high_m1
        Ex_high_m1 = Ex(Ncell-1)

        ! calculate Hy-field
        Hfield: do k = 1, Ncell-1
            Hy(k) = Hy(k) + 0.5 * (Ex(k) - Ex(k+1))
        end do Hfield
        !!! END FDTD !!!
        ! output Ex, Hy
        write(str1, fmt) T
        open(1, file='field/Ex_Hy_'//trim(str1)//'.dat', &
             status='unknown')
        do k = 1, Ncell
            write(1, *) Ex(k), Hy(k)
        end do
        close(1)
    end do steploop


    ! Calculate amplitude and phase of each frequency
    ! Amplitude and phase of the input pulse
    do m = 1, 3
        amp_in(m) = sqrt((imag_in(m) ** 2.0) + &
                         (real_in(m) ** 2.0))
        phase_in(m) = atan2(imag_in(m), real_in(m))
        
        do k = 2, Ncell-1
            ampn(m, k) = (1.0 / amp_in(m)) * &
                         sqrt((real_pt(m, k)) ** 2 + &
                         (imag_pt(m, k)) ** 2)
            phasen(m, k) = atan2(imag_pt(m, k), &
                           real_pt(m, k)) - phase_in(m)
        end do
    end do
    ! write the amplitude field out to files 
    open(2, file='fourier/400step/amp0', status='unknown')
    do k = 1, Ncell
        write(2, *) ampn(1, k)
    end do
    open(3, file='fourier/400step/amp1', status='unknown')
    do k = 1, Ncell
        write(3, *) ampn(2, k)
    end do
    open(4, file='fourier/400step/amp2', status='unknown')
    do k = 1, Ncell
        write(4, *) ampn(3, k)
    end do

    
END PROGRAM main
