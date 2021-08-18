!========================================================
!   Purpose: 1D FDTD simulation in free space with a 
!            Sinusoidal pulse(soft source)
!            with absorbing boundary condition and propagate
!            in a lossy dieletric medium
!
!   Methods: 1D FDTD + absorbing boundary condition
!       
!       Date        Programer       Description of change
!       ====        =========       =====================
!      9/6/20        MorrisH        Original Code
!========================================================
PROGRAM main
    IMPLICIT NONE
    ! number of cells to be used
    INTEGER, PARAMETER :: Ncell = 200
    REAL(8), PARAMETER :: pi = 3.1415927
    REAL(8) :: Ex(Ncell), Hy(Ncell), ca(Ncell), cb(Ncell)
    INTEGER :: k, kc, T, kstart, kfinish
    REAL(8) :: t0, width, pulse, eps, epsz
    REAL(8) :: ddx, dt, freq_in, sigma, eaf
    REAL(8) :: Ex_low_m1 = 0, Ex_high_m1 = 0, &
               Ex_low_m2 = 0, Ex_high_m2 = 0
    REAL(8) :: freq(1000), arg(1000)
    INTEGER(8) :: i, m
    REAL(8) :: real_pt(1000, 2), imag_pt(1000, 2)
    REAL(8) :: real_in(1000, 2), imag_in(1000, 2)
    REAL(8) :: amp_in(1000, 2), phase_in(1000, 2)
    REAL(8) :: ampn(1000, 2), phasen(1000, 2)
    ! name of write file
    CHARACTER(len=15) :: str1
    CHARACTER(len=8) :: fmt
    fmt = '(I4.4)'

    ! initialize field
    Ex = 0.0
    Hy = 0.0
    ! center of the problem space
    kc = Ncell / 2
    ! center of the incident pulse
    t0 = 40.0
    ! width of the incident pulse
    width = 12
    ! initialize in free space
    ca = 1.0
    cb = 0.5
    ! epsilon value
    eps = 4
    epsz = 8.85419E-12
    ! start of dielectric medium
    Kstart = 100
    ! end of dielectric medium
    Kfinish = 160
    ! cell size to 1 m
    ddx = 0.01
    ! time step
    dt = ddx / (2 * 3E8)
    ! frequency of input pulse
    freq_in = 700E6
    ! conductivity
    sigma = 0.00

    eaf = dt * sigma / (2 * epsz * eps)

    ! fourier analysis freqency
    do i = 1, 1000
        freq(i) = real(i) * 1e6
    end do
    arg = 2 * pi * freq * dt


    dielectric: do k = Kstart, Kfinish
        ca(k) = (1.0 - eaf) / (1.0 + eaf)
        cb(k) = 0.5 / (eps * (1.0 + eaf))
    end do dielectric
    
    steploop: do T = 0, 3000

        !!! START FDTD !!!
        ! calculate Ex-field
        Efield: do k = 2, Ncell
            Ex(k) = ca(k) * Ex(k) + cb(k) * (Hy(k-1) - &
                    Hy(k))
        end do Efield
        Ex(50) = Ex(50) - 0.5 * exp(-0.5 * ((t0 - T) / &
                                    width) ** 2.0)

        ! put gaussian pulse in the center
        pulse = exp(-0.5 * ((t0 - T) / width) ** 2.0)
        Ex(50) = Ex(50) + pulse

        ! Calculate the Fourier tramsform of Ex
        do m = 1, 1000
            real_pt(m, 1) = real_pt(m, 1) + cos(arg(m)  &
                            * T)  * Ex(10)
            imag_pt(m, 1) = imag_pt(m, 1) - sin(arg(m) &
                            * T)  * Ex(10)
            real_pt(m, 2) = real_pt(m, 2) + cos(arg(m)  &
                            * T)  * Ex(180)
            imag_pt(m, 2) = imag_pt(m, 2) - sin(arg(m) &
                            * T)  * Ex(180)
        end do
        ! Fourier transform of the input pulse
        if (T < 2 * t0) then
            do m = 1, 1000
                real_in(m, 1) = real_in(m, 1) + &
                                cos(arg(m) * T) * Ex(50)
                imag_in(m, 1) = imag_in(m, 1) - &
                                sin(arg(m) * T) * Ex(50)
                real_in(m, 2) = real_in(m, 2) + &
                                cos(arg(m) * T) * Ex(50)
                imag_in(m, 2) = imag_in(m, 2) - &
                                sin(arg(m) * T) * Ex(50)
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
        Hy(49) = Hy(49) + 0.5 * exp(-0.5 * ((t0 - T + &
                 0.5) / width) ** 2.0)
        !!! END FDTD !!!

        ! output Ex and Hy field
        write(str1, fmt) T
        open(1, file='data/Ex_Hy_'//trim(str1)//'.dat', &
             status='unknown')
        output: do k = 1, Ncell
            write(1, *) Ex(k), Hy(k)
        end do output
        close(1)

        ! output fourier 
        do m = 1, 1000
            do k = 1, 2
                amp_in(m, k) = sqrt((imag_in(m, k) ** &
                               2.0) + (real_in(m, k) ** &
                               2.0))
                phase_in(m, k) = atan2(imag_in(m, k), &
                                       real_in(m, k))
                
                ampn(m, k) = (1.0 / amp_in(m, k)) * &
                             sqrt((real_pt(m, k)) ** 2 + &
                             (imag_pt(m, k)) ** 2)
                phasen(m, k) = atan2(imag_pt(m, k), &
                               real_pt(m, k)) - &
                               phase_in(m, k)
            end do
        end do
        open(2, file='data/reflect'//trim(str1)//'.dat', &
             status='unknown')
        do m = 1, 1000
            write(2, *) ampn(m, 1)
        end do
        close(2)
        open(3, file='data/trans'//trim(str1)//'.dat', &
             status='unknown')
        do m = 1, 1000
            write(3, *) ampn(m, 2)
        end do
        close(3)
    end do steploop 
END PROGRAM main
